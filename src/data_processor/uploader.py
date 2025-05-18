from config.config import settings
import oss2
from pathlib import Path


class Uploader():
    def __init__(self):
        self.auth = oss2.Auth(settings.ACCESS_KEY, settings.ACCESS_KEY_SECRET)
        self.bucket = oss2.Bucket(self.auth, settings.OSS.ENDPOINT, settings.OSS.BUCKET)

    def upload(self):
        # 本地文件路径
        base_path = Path(__file__).resolve().parent.parent / 'data'
        filelist = ['products.csv', 'categories.csv', 'price.csv']  # 需要上传的文件列表
        for file in filelist:
            local_file = os.path.join(base_path, file)  # 本地文件路径
            # 上传文件
            self.bucket.put_object_from_file(oss_key, local_file)
            print(f"已上传至 OSS")


def main():
    uploader = Uploader()
    uploader.upload()


if __name__ == '__main__':
    main()
