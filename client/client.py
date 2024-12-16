import requests
import time

class VideoTranslationClient:
	"""
	Client class for polling the status of a video translation job from a server.

	- serverUrl: Url of where the remote server is running
	- maxRetries: Number of attemps to get the status
	- initialDelay: The initial delay between attempts
	- backoffFactor: The factor that initial delay is increased by after each attempt
	"""
	def __init__(self, serverUrl, maxRetries, initialDelay = 1, backoffFactor = 2):
		self.serverUrl = serverUrl
		self.maxRetries = maxRetries
		self.initialDelay = initialDelay
		self.backoffFactor = backoffFactor

	"""
	Runings for self.maxRetries and gets the status from the server.
	The delay is incremented by a factor of 'backoffFactor' after each attempt
	in order to reduce the cost of calling the server api.
	"""
	def getStatus(self):
		delay = self.initialDelay

		for attempt in range(1, self.maxRetries + 1):
			try:
				response = requests.get(f"{self.serverUrl}/status", timeout=10)
				response.raise_for_status() # raises err for 4xx and 5xx status codes just in case
				result = response.json().get("result", "unknown")
				timeElapsed = response.json().get("timeElapsed", -1)

				print(f"********** Attempt #{attempt}: Status -> {result} **********")
				
				if result == "completed" or result == "error":
					return result, timeElapsed
				elif result != "pending":
					# incase an unexcepted results occurs, we can log and retry
					print(f"Unexpected status '{result}' recieved. Retrying...")
				print(f"Delay: {delay} seconds")
				print(f"Next API call will be made at: {timeElapsed} (time elapsed) + {delay} (delay) = {timeElapsed + delay} seconds")

			except Exception as e:
				print(f"Attempt #{attempt} failed with error: {e}")

			time.sleep(delay)
			delay *= self.backoffFactor

		print("Max retries reached. Exiting as 'failed'.")

		return "failed", -1
  

if __name__ == "__main__":
	serverUrl = "http://127.0.0.1:5000"

	client = VideoTranslationClient(serverUrl=serverUrl, maxRetries=100, initialDelay=1, backoffFactor=2)

	result, timeElapsed = client.getStatus()
	print(f"\nFinal Status: {result}\nTotal time elapsed: {timeElapsed} seconds\n")

	assert result in ["completed", "error"], f"Unexpected final status: {result}"