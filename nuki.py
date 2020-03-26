from smartlock import Smartlock, Pin
from typing import Tuple, List
import requests
import datetime
import utils
import json

class Nuki:
	"""This class contains methods for working with smartlocks from Nuki"""

	def __init__(self, api_key: str, api_url: str):
		self.api_key = api_key
		self.api_url = api_url
	
	def setKey (self, id: int, beginDate: datetime.date, endDate: datetime.date, checkin: datetime.time, checkout: datetime.time, name: str = "pin", debug: bool = False, pin: str = None) -> Tuple[str, bool]:
		"""Sets a key for a lock with the specified id and writes the pin down to the sql database\n
		The pin is returned for further use and a bool if the pin was succesfully set"""
		if pin == None:
			pin = utils.getRandom(1, 9)
			if pin.startswith("12"):
				pin.replace("12", utils.getRandom(1, 9, 2), 1)

		header= {
			'Content-Type': 'application/json',
			'Accept': 'application/json',
			'Authorization': self.api_key
		}

		start = datetime.datetime(beginDate.year, beginDate.month, beginDate.day, checkin.hour, checkin.minute, checkin.second)
		end = datetime.datetime(endDate.year, endDate.month, endDate.day, checkout.hour, checkout.minute, checkout.second)
		
		data = {
			"name": name,
			"type": 13,
			"code": int(pin),
			"allowedFromDate": utils.buildDateString(start),
			"allowedUntilDate": utils.buildDateString(end),
			"allowedWeekDays": 127,
		}

		if debug:
			print("header:", header)

		if debug:
			print("data:", data)

		back = None
		url = self.api_url + "smartlock/" + str(id) + "/auth"

		if not debug:
			back = requests.put(url, headers=header, data=json.dumps(data))
			if back.ok:
				succesfull = True
			else:
				print("Set key on " + str(id) + " didn't succeded additional infos:")
				print("Reason: " + str(back.reason))
				print("Status Code: " + str(back.status_code))
				succesfull = False
		else:
			succesfull = True

		return pin, succesfull


	def getSmartlockByName (self, name: str) -> Smartlock:
		"""Gets a smartlock by name and returns the specific object"""
		locks = self.getAllLocks()

		for lock in locks:
			if lock.name.lower().find(name.lower()) != -1:
				return lock
		return None
	

	def getSmartlockByID (self, id: str) -> Smartlock:
		"""Gets a smartlock by name and returns the specific object"""
		locks = self.getAllLocks()

		for lock in locks:
			print("")
			if lock.id == id:
				return lock
		return None


	def getAllLocks(self) -> List[Smartlock]:
		"""Gets all locks and convert them into a list of smartlocks\n
		If an error occurs, `None` is returned"""
		header = {"Authorization": self.api_key, "Accept": "application/json"}
		back = requests.get(self.api_url + "smartlock", headers=header)
		json = back.json()

		smartlocks = []
		if "detailMessage" in json:
			return None


		for key in json:
			smartlocks.append(Smartlock(str(key['smartlockId']), key['name']))

		return smartlocks

	def getPin(self, lock_id: int, pin_name: str, debug: bool = False) -> Pin:
		"""Searches for the pin on the smartlock specified with `lock_id` and filters for pin_name\n
		Returns a `pin` object"""
		header = {"Authorization": self.api_key, "Accept": "application/json"}
		req = requests.get(self.api_url + "smartlock/" + str(lock_id) + "/auth", headers=header)
		json = req.json()
		for key in json:
			if key["name"] == pin_name:
				try:
					lastActiveDate = utils.strToDateTime(key["lastActiveDate"])
				except KeyError:
					lastActiveDate = None
		
				creationDate = utils.strToDateTime(key["creationDate"])
				updateDate = utils.strToDateTime(key["updateDate"])

				if debug:
					utils.printJson(json)

				try:
					code = key["code"]
				except Exception:
					code = "No Pin available"

				return Pin(key["id"], key["smartlockId"], key["authId"], int(key["type"]), key["name"], bool(key["enabled"]), bool(key["remoteAllowed"]), int(key["lockCount"]), lastActiveDate, creationDate, updateDate, code)
		return None

	
	def getAllPins(self, lock_id: str) -> List[Pin]:
		"Returns all pins in a smartlock specified by `lock_id` and returns them in a list of `Pin` objects"
		header = {"Authorization": self.api_key, "Accept": "application/json"}
		req = requests.get(self.api_url + "smartlock/" + lock_id + "/auth", headers=header)
		json = req.json()
		pins = []
		for pin in json:
			try:
				lastActiveDate = utils.strToDateTime(pin["lastActiveDate"])
			except KeyError:
				lastActiveDate = None
		
			creationDate = utils.strToDateTime(pin["creationDate"])
			updateDate = utils.strToDateTime(pin["updateDate"])
			
			try:
				code = str(pin["code"])
			except KeyError:
				code = "No Pin available"

			p = Pin(pin["id"], pin["smartlockId"], pin["authId"], int(pin["type"]), pin["name"], bool(pin["enabled"]), bool(pin["remoteAllowed"]), int(pin["lockCount"]), lastActiveDate, creationDate, updateDate, code)
			pins.append(p)
		return pins


	def deletePin(self, smartlock_id: str, pin_id: str) -> bool:
		"""Deletes the pin on `smartlock_id` with the id `pin_id`\n
		Returns true if succesfull"""
		header = {"Authorization": self.api_key, "Accept": "application/json"}
		req = requests.delete(self.api_url + "smartlock/" + smartlock_id + "/auth/" + pin_id, headers=header)
		return req.ok

	
	def deactivatePin(self, smartlock_id: str, pin_id: str) -> Tuple[bool, list]:
		"""Deactivates (not deleting) a pin on the device specified with `smartlock_id` and the pin specified with `pin_id`"""
		header = {"Authorization": self.api_key, "Accept": "application/json", "Content-Type": "application/json"}
		data = { "enable": False }
		req = requests.post(self.api_url  + "smartlock/" + smartlock_id + "/auth/" + pin_id, headers=header, data=data)
		return req.ok


	def updatePin(self, smartlock_id: str, pin_id: str, new_values: dict) -> Tuple[bool, list]:
		"""Updates the pin with id `pin_id` on the device with id `smartlock_id` and the `new_values`\n
		It returns a bool containing whether it was succesfull or not """
		header = {"Authorization": self.api_key, "Accept": "application/json", "Content-Type": "application/json"}
		req = requests.post(self.api_url + "smartlock/" + smartlock_id + "/auth/" + pin_id, headers=header, data=json.dumps(new_values))

		return req.ok