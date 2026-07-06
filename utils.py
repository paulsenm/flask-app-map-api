import math

SEPARATOR_ = '+'
CODE_ALPHABET_ = '23456789CFGHJMPQRVWX'
SIZE = 11

def EncodeLatLonSize(lat, lon):
	code = ''
	digit11 = ''
	nextLatChar = 0
	nextLonChar = 0
	
	xMul = 8000
	yMul = 8000
	if SIZE >= 11:
		xMul *= 4
		yMul *= 5
	if SIZE >= 12:
		xMul *= 4
		yMul *= 5
		
	currentLat = int(math.floor((lat + 90) * yMul))
	currentLon = int(math.floor((lon + 180) * xMul))
		
	if SIZE >= 12:
		nextLonIndex = (currentLon % 4) 
		nextLatIndex = (currentLat % 5)
		indexDigit = (nextLatIndex * 4 + nextLonIndex)
		digit11 = CODE_ALPHABET_[indexDigit] + digit11
		currentLat = math.floor(currentLat / 5)
		currentLon = math.floor(currentLon / 4)
		
	if SIZE >= 11:
		nextLonIndex = (currentLon % 4) 
		nextLatIndex = (currentLat % 5)
		indexDigit = (nextLatIndex * 4 + nextLonIndex)
		digit11 = CODE_ALPHABET_[indexDigit] + digit11
		currentLat = math.floor(currentLat / 5)
		currentLon = math.floor(currentLon / 4)
	
	for i in range(5):
		nextLonChar = (currentLon % 20)
		nextLatChar = (currentLat % 20)
		
		code = CODE_ALPHABET_[nextLatChar] + CODE_ALPHABET_[nextLonChar] + code
		currentLat = math.floor(currentLat / 20)
		currentLon = math.floor(currentLon / 20)

	code = code + digit11
	
	return code