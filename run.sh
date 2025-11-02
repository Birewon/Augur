#!/bin/bash

echo " ____                  __  ______                    ";
echo "/\\  _\`\\               /\\ \\/\\  _  \\                   ";
echo "\\ \\ \\L\\ \\_ __    __   \\_\\ \\ \\ \\L\\ \\  _____   _____   ";
echo " \\ \\ ,__/\\\`'__\\/'__\`\\ /'_\` \\ \\  __ \\/\\ '__\`\\/\\ '__\`\\ ";
echo "  \\ \\ \\/\\ \\ \\//\\  __//\\ \\L\\ \\ \\ \\/\\ \\ \\ \\L\\ \\ \\ \\L\\ \\";
echo "   \\ \\_\\ \\ \\_\\\\ \\____\\ \\___,_\\ \\_\\ \\_\\ \\ ,__/\\ \\ ,__/";
echo "    \\/_/  \\/_/ \\/____/\\/__,_ /\\/_/\\/_/\\ \\ \\/  \\ \\ \\/ ";
echo "                                       \\ \\_\\   \\ \\_\\ ";
echo "                                        \\/_/    \\/_/ ";


if [[ $1 == "--help" ]]; then
	echo "Help information:"
	echo "There will be useful information here"
	exit

elif [[ $1 == "del_venv" ]]; then
	rm -rf $PWD/PredictiveAnalyticsApp_v.0.0.0-venv
	printf "\n[+]: Virtual environment has been deleted.\n\n"
	exit
fi

if [ -d "$PWD/PredictiveAnalyticsApp_v.0.0.0-venv" ]; then
	echo "[*]: Activate Python virtual env..."
	source $PWD/PredictiveAnalyticsApp_v.0.0.0-venv/bin/activate &>-
	echo "[+]: Done"
	echo "[*]: Starting..."
	python3.12 main.py
else
	response=""
	read -r -p "You don’t have a virtual environment, do you want to create it and download all dependencies? (Y/N): " response
	response=${response^^}

	if  [[ "$response" == "Y" ]]; then
		echo "[*]: Updating..."
		sudo apt update
		echo "[+]: Done"

		printf "\n[*]: Installing python3.12\n"

		sudo apt update -y
		sudo apt upgrade -y

		sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5 xz-utils tk-dev libffi-dev liblzma-dev python-openssl

		wget https://www.python.org/ftp/python/3.12.1/Python-3.12.1.tgz

		tar -xf Python-3.12.1.tgz
		cd Python-3.12.1
		sudo ./configure --enable-optimizations
		sudo make altinstall
		cd ..
		printf "\n\n[+]: Creating virtual environment..."
		python3.12 -m venv PredictiveAnalyticsApp_v.0.0.0-venv
		echo "[+]: Done"

		echo "[*]: Activating venv..."
		source $PWD/PredictiveAnalyticsApp_v.0.0.0-venv/bin/activate
		echo "[+]: Done"

		echo "[*]: Updating pip..."
		pip install --upgrade pip
		echo "[+]: Done"

		echo "[*]: Downloading all dependencies..."
		pip install -r requirements.txt
		echo "[+]: Done"

		echo "[+]: Successful installation!"

		echo "[*]: Starting..."
		python3.12 main.py
	fi
fi

echo "done!"

echo "Hello! If you have any questions about the program, you can ask them here:"
echo "https://github.com/Birewon/PredictiveAnalyticsApp/issues"
