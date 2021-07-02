**5/1/2021**
I will be using the API from (https://www.govinfo.gov/) to pull transcripts and move them into an S3 bucket.
This is mainly for me to practice using Airflow and AWS, but I am pretty sure there's something cool in this data.

**7/1/2021**
After a couple months of not much progress, I'm finally at a good stopping point! I have an EC2 instance running
the puckel Airflow image, which runs a docker image containing this code every day. The results are getting uploaded
into an S3 bucket. The next steps for me will be to perform further cleaning and hopefully some analysis on the data.
