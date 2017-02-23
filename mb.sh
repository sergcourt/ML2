#!/bin/bash

if [ "$#" -lt 3 ]; then
   echo "Usage:  ./dfcimb.sh needs at least 3 arguments: customer_ID, email, file to upload "
   echo "   eg:  ./dfci.sh somebody_ID somebody@gmail.com  filepath/file for single files or filepath/* for multile files"
   exit
fi

CUSTOMER_ID=$1
# shift
EMAIL=$2
# shift
FILES=$3
PREFIX='dfci-'

echo "verifying bucket name a availability..."
gsutil ls -b gs://${PREFIX}${CUSTOMER_ID} || gsutil mb -c regional -l us-central1 gs://${PREFIX}${CUSTOMER_ID}

echo "recursively copying all your folder files..."
gsutil -m cp -r $3$i gs://${PREFIX}${CUSTOMER_ID}/$i


# gsutil -m cp -r  $3 gs://${PREFIX}${CUSTOMER_ID}
echo "adding your customer with reading permission on the bucket ..."

gsutil acl ch -u ${EMAIL}:READ gs://${PREFIX}${CUSTOMER_ID}

echo "Enabling  acces logs on your bucket..." 
gsutil logging set on -b gs://svlogbucket -o ${CUSTOMER_ID}-AccessLog  gs://${PREFIX}${CUSTOMER_ID}

echo "creating a copy of bucket ACLs in your origin folder..."
gsutil acl get gs://${PREFIX}${CUSTOMER_ID} > demo/test1ACL.txt

OBJECTS=$(gsutil ls -r gs://${PREFIX}${CUSTOMER_ID})

echo -e "These are the objects succesfully uploaded:\n$OBJECTS" 

 



# grep -v gs://${PREFIX}${CUSTOMER_ID} $4 | $5
# sudo at now +8 hours gsutil acl ch -d ${EMAIL} gs://${PREFIX}${CUSTOMER_ID}


echo "This Customer facing URL will expire in 48 hours: https://storage.googleapis.com/${PREFIX}${CUSTOMER_ID}/$3"

