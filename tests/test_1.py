import pytest
import subprocess
import time
import os
from client.client import VideoTranslationClient

@pytest.fixture(scope="module")
def serverProcess():
	env = os.environ.copy()
	process = subprocess.Popen(["python3", "server/server.py"], env=env)
	time.sleep(1) # to give server some time to start
	yield process
	process.terminate()

def test_1(serverProcess):
	localUrl = "http://127.0.0.1:5000"

	client = VideoTranslationClient(serverUrl=localUrl, maxRetries=100, initialDelay=1, backoffFactor=2)

	result, timeElapsed = client.getStatus()
	print(f"\nFinal Status: {result}\nTotal time elapsed: {timeElapsed} seconds\n")
	
	assert result in ["completed", "error"], f"Unexpected final status: {result}"
