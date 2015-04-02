#!/usr/bin/env ruby

# Name: alien_wallpaper.rb
# Description: Downloads top images from specified subreddits.
# Author: Bob Gardner
# Updated: 4/1/15
# License: MIT

require 'json'
require 'net/http'
require 'open-uri'
require 'optparse'

# The default subreddits to download images from.
DEFAULT_SUBREDDITS = <<-EOS
ArchitecturePorn,CityPorn,EarthPorn,SkyPorn,spaceporn,winterporn,quoteporn
EOS

USER_AGENT = <<-EOS
Alien Wallpaper: A beautiful desktop wallpaper downloader for Reddit by
/u/Wolf_Blackout.
EOS

# Supported file types.
FILE_EXTENSION_REGEX = /\.(jpg|jpeg|gif|png)$/i

# The command line options.
options = { n: 25, out: Dir.pwd, subreddits: DEFAULT_SUBREDDITS.strip }

optparse = OptionParser.new do |opts|
  opts.on('-n N', Integer, 'Number of images to download for each subreddit') \
          do |n|
    options[:n] = n
  end
  opts.on('-o', '--out DIR', String, 'Directory to save wallpaper to') do |out|
    options[:out] = out
  end
  opts.on('-s', '--subreddits S', String, 'Comma separated subreddits to' \
         'download images from; the defaults are SFW') do |s|
    options[:s] = s
  end
  opts.on('-h', '--help', 'Display this screen') do
    puts 'Download beautiful wallpaper from subreddits'
    puts opts
    exit
  end
end
optparse.parse!

# The filename to save the post's image as.
#   precondition: post's image is a supported filetype.
def filename(post)
  post['data']['id'] + post['data']['url'].match(FILE_EXTENSION_REGEX)[0]
end

# Ignore nil, self posts, and unsupported images.
def ignore_post?(post)
  return true if post.nil?
  return true if post['data']['is_self']
  return false if post['data']['url'].match(FILE_EXTENSION_REGEX)
  $stderr.puts post['data']['url']
  true
end

# Download the image associated with the Reddit post.
def download_image(post, output_dir)
  # Construct the filename and filepath
  filepath = File.join(output_dir, filename(post))
  puts filepath

  # Need to use write-binary (wb) mode for images
  begin
    File.open(filepath, 'wb') { |f| f << open(post['data']['url']).read }
  rescue OpenURI::HTTPError => error
    $stderr.puts error
  rescue OpenSSL::SSL::SSLError => error
    $stderr.puts error
  end
end

# Download top 25 images for a given subreddit.
def download_images_for_subreddit(subreddit, out_dir)
  url = URI("http://www.reddit.com/r/#{subreddit}.json")
  req = Net::HTTP::Get.new(url, 'User-Agent' => USER_AGENT)
  res = Net::HTTP.start(url.host, url.port) { |http| http.request(req) }

  json = JSON.parse(res.body)
  json['data']['children'].each do |post|
    download_image(post, out_dir) unless ignore_post?(post)
  end
end

def internet_connection?
  true if open('http://www.google.com/')
rescue
  false
end

def main(opts)
  abort('No Internet connection available.') unless internet_connection?

  threads = []
  opts[:subreddits].split(',').each do |subreddit|
    threads << Thread.new do
      download_images_for_subreddit(subreddit, opts[:out])
    end
  end
  threads.each(&:join)
end

main(options)
