from utils.utils import step_already_finished, should_execute_step, generate_app_data
from database.database import save_progress, save_feature
from logger.logger import logger
from const.function_calls import DEVELOPMENT_PLAN
from templates import apply_project_template
from utils.exit import trace_code_event

class TechLead:
    DEVELOPMENT_PLANNING_STEP = 'development_planning'

    def __init__(self, project):
        self.project = project
        self.convo = AgentConvo(self)
        self.save_dev_steps = False

    def create_development_plan(self):
        """Create a development plan for the project."""
        self.project.current_step = self.DEVELOPMENT_PLANNING_STEP

        step = get_progress_steps(self.project.args['app_id'], self.DEVELOPMENT_PLANNING_STEP)
        if step and not should_execute_step(self.project.args['step'], self.DEVELOPMENT_PLANNING_STEP):
            step_already_finished(self.project.args, step)
            self.project.development_plan = step['development_plan']
            return

        existing_summary = apply_project_template(self.project)

        print(color_green_bold("Starting to create the action plan for development...\n"), category='agent:tech-lead')
        logger.info("Starting to create the action plan for development...")

        try:
            self.project.development_plan = self.convo.send_message('development/plan.prompt', self.get_plan_prompt_args())
        except Exception as e:
            logger.error(f"Error creating development plan: {e}")
            trace_code_event()
            raise

        logger.info('Plan for development is created.')

        save_progress(self.project.args['app_id'], self.project.current_step, {
            "development_plan": self.project.development_plan, "app_data": generate_app_data(self.project.args)
        })

    def create_feature_plan(self, feature_description):
        """Create a plan for developing a new feature."""
        self.save_dev_steps = True

        try:
            self.project.development_plan = self.convo.send_message('development/feature_plan.prompt', self.get_feature_plan_prompt_args(feature_description))
        except Exception as e:
            logger.error(f"Error creating feature plan: {e}")
            trace_code_event()
            raise

        logger.info('Plan for feature development is created.')

    def create_feature_summary(self, feature_description):
        """Create a summary for a new feature."""
        self.save_dev_steps = True

        try:
            self.project.feature_summary = self.convo.send_message('development/feature_summary.prompt', self.get_feature_summary_prompt_args(feature_description))
        except Exception as e:
            logger.error(f"Error creating feature summary: {e}")
            trace_code_event()
            raise

        if not self.project.skip_steps:
            save_feature(self.project.args['app_id'],
                         self.project.feature_summary,
                         self.convo.messages,
                         self.project.checkpoints['last_development_step']['id'])

        logger.info('Summary for new feature is created.')

    def get_plan_prompt_args(self):
        """Return arguments for the development plan prompt."""
        return {
            "name": self.project.args['name'],
            "app_type": self.project.args['app_type'],
            "app_summary": self.project.project_description,
            "user_stories": self.project.user_stories,
            "user_tasks": self.project.user_tasks,
            "architecture": self.project.architecture,
            "technologies": self.project.system_dependencies + self.project.package_dependencies,
            "existing_summary": self.project.existing_summary,
            "files": self.project.get_all_coded_files(),
            "task_type": 'app',
        }

    def get_feature_plan_prompt_args(self, feature_description):
        """Return arguments for the feature plan prompt."""
        return {
            **self.get_plan_prompt_args(),
            "directory_tree": self.project.get_directory_tree(True),
            "previous_features": self.project.previous_features,
            "feature_description": feature_description,
            "task_type": 'feature',
        }

    def get_feature_summary_prompt_args(self, feature_description):
        """Return arguments for the feature summary prompt."""
        return {
            "name": self.project.args['name'],
            "app_type": self.project.args['app_type'],
            "app_summary": self.project.project_description,
            "feature_description": feature_description,
            "development_tasks": self.project.development_plan,
        }
