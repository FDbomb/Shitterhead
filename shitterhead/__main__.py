from sys import argv
import app

if __name__ == '__main__':
	if argv[1] == '-s':
		app.run()
	else:
		app.receive()
