import os
class Constants:
    MIN_KUBECTL_VERSION = "1.28.0"
    ONE_DAY = 86400

    CONFIG_FILE_PATH = os.path.expanduser("~/.k8st/config.json")
    LOG_FILE_PATH = os.path.expanduser("~/.k8st/k8st.log")
