from etl_manager.etl import GlueJob
import os

ROLE = 'name_of_iam_role_for_glue_job_to_assume'

bucket = 's3_bucket_where_job_python_file_and_jar_will_go'

job = GlueJob('glue_job/', bucket=bucket, job_role=ROLE,
              job_arguments={'--enable-spark-ui': 'true',
                             '--spark-event-logs-path': 's3://path_to_logs',
                             '--enable-continuous-cloudwatch-log': 'true',
                             '--enable-metrics': ''})

job.job_name = 'my_job_name'

job.allocated_capacity = 4

try:
    job.run_job()
    job.wait_for_completion()
finally:
    job.cleanup()