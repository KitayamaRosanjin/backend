#!/usr/bin/env python3
import aws_cdk as cdk
from backend_stack import BackendStack

app = cdk.App()
# 先ほど Gemini と一緒に作った BackendStack クラスを呼び出します
BackendStack(app, "BackendStack")

app.synth()