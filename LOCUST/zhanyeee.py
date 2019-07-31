from locust import HttpLocust, TaskSet, task
url = "http://twork.zhanye.api.youxin.info:44752/api/v/1.0/auth/sms_codes"
data = {"mobile": "13776665555"}

class Mytest_perface(TaskSet):
    """蝗虫类"""

    @task
    def test_login(self):
        self.client.post(url, data)

class WebsiteUser(HttpLocust):
    task_set = Mytest_perface
    min_wait = 0
    max_wait = 0

