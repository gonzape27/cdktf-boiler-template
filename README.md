Project: cdktf-boiler-template
--------------------------

Deploying infrastructure with Terraform CDK.  


Requirements:
-------------

[NODEJS]

curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g cdktf-cli

[PYTHON]

python3 -m venv virtualenv
source virtualenv/bin/activate
cd learn-cdktf-python
pip3 install -r requirements.txt

[.gitignore]

* virtualenv
* TCDK imports folder
* Terraform tfstate files
