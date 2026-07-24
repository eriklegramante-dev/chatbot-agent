import litellm
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

os.environ["LITELLM_DROP_PARAMS"] = "True"
litellm.drop_params = True
