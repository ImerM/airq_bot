## Air Quality Twitter Bot

This is a simple serverless application that creates plots and graphics based on data taken from the air quality monitors installed by the US Embassy in Sarajevo. If you have a Twitter developer account, and have generate the appropriate keys you can deploy your own bot.

This is a collection of AWS Lambda functions that are managed by a AWS Step Function, and scheduled to run every hour via AWS CloudWatch. If you wish to deploy the app yourself you need to create each lambda function separately, and bundle it together with their dependencies, [a guide on how to do se can be found here](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html).

The dependencies are :
1) Feedparser - feed_parser function
1) Numpy & matplotlib - make_hist function
1) Pillow and Numpy - merge_images function
1) Pillow - write_on_img function
1) Twython - publish_to_tw function

Other imported libraries are already available through AWS Lambda, so there is no need to import them.

All functions except for 'feed_parser' rely on the following environmental variables being set:

1) make_hist - REGION_HOST, S3_BUCKET
1) merge_images - REGION_HOST, S3_BUCKET
1) write_on_img - REGION_HOST, S3_BUCKET
1) publish_to_tw - REGION_HOST, S3_BUCKET, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET

You will need to have an S3 bucket created, where you can copy the 'assets' folder into. It contains the font to use, as well as the basic templates used for writing the AQI values. Specify the name of the bucket and the region it is in as the env values for S3_BUCKET, and REGION_HOST, respectively.

Once you have created the lambda functions, with the dependencies included, you can proceed to create the state machine. It does not depend on any user input. The cloudfront template is provided as 'state_machine.yml'. In case of any errors please open the cloudfront template designer, and validate it there as the YAML format can have odd validation issues.

You can either start the step function from the step functions console, or set it to run periodically using cloud watch.

[This is a great guide for genomics on AWS, it helped me understand lambda and SF much better](https://aws.amazon.com/blogs/compute/building-high-throughput-genomics-batch-workflows-on-aws-workflow-layer-part-4-of-4/). For guides into using AWS Lambda and other services please consult their documentation.

[The bot can be found on Twitter](https://twitter.com/KvalitetaS), [and so can I](https://twitter.com/ImerM1).