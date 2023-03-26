curl https://seekingalpha.com/symbol/SP500 > /home/ec2-user/Linux_Project/SP500.txt
current_price=$(cat /home/ec2-user/Linux_Project/SP500.txt |grep -oP '(?<=data-test-id="symbol-price">\$<!-- -->)[0-9,]+\.[0-9]{2}' | sed 's/\,/ /')
current_time=$(date +"%Y-%m-%d %H:%M:%S")
echo $current_price
echo $current_time
echo "$current_price,$current_time" >> /home/ec2-user/Linux_Project/data1.csv
