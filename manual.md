##Manual

###Install mongodb
Linux(Ubuntu/Debian)
		
		sudo apt-get update
		sudo apt-get install -y mongodb-org
		
OS X

		brew update
		brew install mongodb
		
Or follow the guides on the official website: [mongodb](http://docs.mongodb.org/manual/)


###import database

####unzip datafiles

		adsdata.zip -> adsdata/
		
####run mongodb

 1. OS X
 	
 		mkdir /data/db  # if not exist
 		mongod
 		
 2. Linux
 		
 		sudo service mongod start
	
to stop:
 
 		# sudo servercie mongod stop
 		
####import datafiles

 		mongorestore -d adsdata --directoryperdb [PathDatafiles]
 		
 		# PathDatafiles is the path of the directory you have just unzipped
 		#Database name(ads data) must not be changed! Or the code will not work
 		
 
###install requirements
unzip code.zip

	cd code/
	sudo pip install	-r requirements.txt

###run the code

	python GUI.py
	
	
##Usage
Initial GUI
![](/Users/feiyicheng/Dropbox/屏幕截图/屏幕截图 2015-04-26 12.41.25.png)
Choose a mol file
![](/Users/feiyicheng/Dropbox/屏幕截图/屏幕截图 2015-04-26 12.41.51.png)
![](/Users/feiyicheng/Dropbox/屏幕截图/屏幕截图 2015-04-26 12.42.04.png)
file loaded successfully
![](/Users/feiyicheng/Dropbox/屏幕截图/屏幕截图 2015-04-26 12.42.15.png)
submit and it will be running for about 10 seconds
![](/Users/feiyicheng/Dropbox/屏幕截图/屏幕截图 2015-04-26 12.42.25.png)
some molecules with high similarity with the input will be shown
![](/Users/feiyicheng/Dropbox/屏幕截图/屏幕截图 2015-04-26 12.42.42.png)
close-up
![](/Users/feiyicheng/Dropbox/屏幕截图/屏幕截图 2015-04-26 12.42.55.png)


PS:
It's just a prototype and we are adding more functions.
And if you find some bugs or need some specific functions. Welcome to tell us <fycisc@mail.ustc.edu.cn>

<zsl712@mail.ustc.edu.cn>

<wcya462@mail.ustc.edu.cn>

The up-to-date codes can be accessed on [https://github.com/fycisc/ads](https://github.com/fycisc/ads)



