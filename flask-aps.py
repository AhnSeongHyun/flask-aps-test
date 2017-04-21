from flask import Flask
from flask_apscheduler import APScheduler
from datetime import datetime, timedelta


class Config(object):
    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }

    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 3
    }

    SCHEDULER_API_ENABLED = True


if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(Config())

    def tick(*args):
        print 'args : ' + str(args) + "\t"+ str(datetime.now()) + ' - tick'


    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.scheduler = scheduler

    @app.route("/register/<string:job_name>")
    def register(job_name):
        try:
            app.scheduler.add_job(id=job_name,
                                  func=tick, trigger='date',
                                  args=['param1', 'param2'],
                                  run_date=datetime.now() + timedelta(seconds=10))
            print app.scheduler.get_jobs()
            return "register : " + job_name
        except:
            import traceback
            print traceback.format_exc()


    @app.route("/remove/<string:job_name>")
    def remove(job_name):
        try:
            app.scheduler.delete_job(job_name)
            print app.scheduler.get_jobs()
            return "remove : " + job_name
        except:
            import traceback
            print traceback.format_exc()


    @app.route("/status")
    def status():
        try:
            print app.scheduler.get_jobs()
            return str(app.scheduler.get_jobs())
        except:
            import traceback
            print traceback.format_exc()

    app.run()