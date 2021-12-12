# Final Implementation
For my final approach, I explore the results from https://index.commoncrawl.org/ and how I could use it for my solution. Finally, I was able to extract the links from the results for 2020 which I crawled using requests.get() to get the content of all the sites and if the content had sufficient number of occurences related to `covid-19` and `economy`, I print the link it belongs to and from which month I extracted it. 

# Initial Approach
My initial approach was to scan through and open every article using the sample implementation provided by TrustLab. I was able to print the HTML content but while storing it to a list, it was not getting append(Not sure why!)

# Assumptions
1. The pages should be from a trusted and most popular news site
2. The pages should mention covid-19 about 20 times
3. The pages should also mention economic factors about 5 times