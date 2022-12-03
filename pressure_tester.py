# /usr/bin python3
# encoding: utf-8

import os
from locust import HttpUser
from locust import task

USER = '0x44C3fD4C61d17d199270e0b1CB9121BfF49E7895'

class PressureTester(HttpUser):
    def on_start(self):
        print("on starting")

    def on_stop(self):
        print("on stopping")

    def _get(self, name, url):
        with self.client.get(url=url, name=name, catch_response=True) as res:
            try:
                err = res.json().get('errmsg')
            except Exception as e:
                res.failure(f'Response Err: {res.text} || {e.msg}')
                # exit(f'Response Err: {e.msg}')
            else:
                if (not err) and res.status_code==200:
                    res.success()
                else:
                    res.failure(f'StatusCode[{res.status_code}]: {err}')

    def _post(self, name, url, data={}):
        with self.client.post(url=url, data=data, name=name, catch_response=True) as res:
            code = res.json()['code']
            if code==0 and res.status_code==200:
                res.success()
            else:
                res.failure(f'StatusCode[{res.status_code}]: code={code}')


    # @task
    # def current_week(self):
    #     self._get(
    #         "get current week",
    #         "/api/v1/trade-mine/current-week"
    #     )

    # @task
    # def next_week(self):
    #     self._get(
    #         "get next week",
    #         "/api/v1/trade-mine/next-week"
    #     )

    # @task
    # def campaign_info(self):
    #     self._get(
    #         "get campaign info",
    #         "/api/v1/trade-mine/campaign-info"
    #     )

    ## config
    @task
    def period_info(self):
        self._get(
            "get period info",
            "/api/v1/trade-mine/period-info"
        )
    @task
    def contracts(self):
        self._get(
            "get contracts info",
            "/api/v1/trade-mine/contracts"
        )
    @task
    def constants(self):
        self._get(
            "get constants info",
            "/api/v1/trade-mine/constants"
        )


    ## score
    @task
    def score(self):
        self._get(
            "get score and reward",
            "/api/v1/trade-mine/score?ethAddress="+USER
        )
    @task
    def score_by_wallet(self):
        self._get(
            "get score by ethAddress",
            "/api/v1/trade-mine/score-by-wallet?ethAddress="+USER
        )
    @task
    def score_sum(self):
        self._get(
            "get score and reward sum",
            "/api/v1/trade-mine/score-sum"
        )

    ## claim
    @task
    def last_sign(self):
        self._get(
            "get sign record",
            "/api/v1/trade-mine/last-sign?ethAddress="+USER
        )
    @task
    def sign_record(self):
        self._get(
            "get sign record",
            "/api/v1/trade-mine/sign-record?ethAddress="+USER
        )

    ## holding
    @task
    def fee_snapshot(self):
        self._get(
            "get fee",
            "/api/v1/trade-mine/fee-snapshot"
        )
    @task
    def position_snapshot(self):
        self._get(
            "get position",
            "/api/v1/trade-mine/position-snapshot"
        )
    @task
    def filltransactions(self):
        self._get(
            "get fill transactions",
            "/api/v1/trade-mine/filltransactions"
        )
    @task
    def holding_records(self):
        self._get(
            "get holding records",
            "/api/v1/trade-mine/holding-records?ethAddress="+USER
        )

    ## graphql
    @task
    def rate_logs(self):
        self._get(
            "get bana-apex rate logs",
            "/api/v1/trade-mine/graph/banana-apex-rate-logs"
        )
    @task
    def claim_logs(self):
        self._get(
            "get bana claim logs",
            "/api/v1/trade-mine/graph/banana-claim-logs"
        )
    @task
    def actions_logs(self):
        self._get(
            "get banana user actions logs",
            "/api/v1/trade-mine/graph/banana-user-actions-logs"
        )
    @task
    def kline_logs(self):
        self._get(
            "get kline logs",
            "/api/v1/trade-mine/graph/kline-logs"
        )
    @task
    def transfer_logs(self):
        self._get(
            "get transfer logs",
            "/api/v1/trade-mine/graph/transfer-logs?first=1"
        )
    @task
    def usdc_spents(self):
        self._get(
            "get usdc total spents",
            "/api/v1/trade-mine/graph/usdc-total-spents"
        )
    @task
    def total_gains(self):
        self._get(
            "get usder action total gains",
            "/api/v1/trade-mine/graph/user-action-total-gains"
        )




    # ## Airdrop Page
    # def airdrop_config(self):
    #     self._post(
    #         "get airdrop config",
    #         "/api/airdrop/getAirdropConfig"
    #     )

    # def get_player(self):
    #     self._post(
    #         "get player info",
    #         "/api/airdrop/getPlayer",
    #         {"my_wallet": USER}
    #     )

if __name__ == '__main__':
    os.system("locust -f bana.py --web-host=127.0.0.1")
