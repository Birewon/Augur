#!/bin/bash

echo ""
echo ""
echo " █████╗ ██╗   ██╗ ██████╗ ██╗   ██╗██████╗ ";
echo "██╔══██╗██║   ██║██╔════╝ ██║   ██║██╔══██╗";
echo "███████║██║   ██║██║  ███╗██║   ██║██████╔╝";
echo "██╔══██║██║   ██║██║   ██║██║   ██║██╔══██╗";
echo "██║  ██║╚██████╔╝╚██████╔╝╚██████╔╝██║  ██║";
echo "╚═╝  ╚═╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝";
echo "                                           ";
echo "Created by: Birewon    PredApp v.1.0.1-beta"
echo "                           "
echo ""

if [[ $1 == "--help" ]]; then
	echo "Help information:\n"
	echo "Launch/Install --> ./run.sh"
	echo "Delete --> ./run.sh --del_venv"
	exit

elif [[ $1 == "--del_venv" ]]; then
	rm -rf $PWD/Augur_v.0.0.0-venv
	printf "\n[+]: Virtual environment has been deleted.\n\n"
	exit
fi

if [ -d "$PWD/Augur_v.0.0.0-venv" ]; then
	echo "[*]: Activate Python virtual env..."
	source $PWD/Augur_v.0.0.0-venv/bin/activate &>-
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
		python3.12 -m venv Augur_v.0.0.0-venv
		echo "[+]: Done"

		echo "[*]: Activating venv..."
		source $PWD/Augur_v.0.0.0-venv/bin/activate
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

echo "If you have any questions about the program, you can ask them here:"
echo "https://github.com/Birewon/Augur/issues"
