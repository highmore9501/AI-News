import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models
import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()


# 这里用的是腾讯的机器翻译api，需要注册腾讯云账号并开通机器翻译服务
class Translater(object):
    def __init__(self) -> None:
        self.SecretId = os.getenv("SecretId")
        self.SecretKey = os.getenv("SecretKey")
        self.cred = credential.Credential(self.SecretId, self.SecretKey)
        self.httpProfile = HttpProfile()
        self.httpProfile.endpoint = "tmt.tencentcloudapi.com"
        self.clientProfile = ClientProfile()
        self.clientProfile.httpProfile = self.httpProfile
        self.client = tmt_client.TmtClient(
            self.cred, "ap-guangzhou", self.clientProfile)
        self.req = models.TextTranslateRequest()

    def translate(self, text: str, source: str, target: str) -> str:
        params = {
            "SourceText": text,
            "Source": source,
            "Target": target,
            "ProjectId": 0
        }
        try:
            self.req.from_json_string(json.dumps(params))
            resp = self.client.TextTranslate(self.req)
            return resp.TargetText
        except TencentCloudSDKException as err:
            print(err)
            return ""


if __name__ == "__main__":
    translater = Translater()
    print(translater.translate("this is a hippo", "en", "zh"))
