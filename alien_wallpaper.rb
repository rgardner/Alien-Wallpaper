#!/usr/bin/env ruby

# Name: alien_wallpaper.rb
# Description: Downloads top 25 images from specified subreddits.
# Author: Bob Gardner
# Updated: 8/23/14
# License: MIT

require 'json'
require 'net/http'
require 'open-uri'
require 'trollop'

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
  File.open(filepath, 'wb') { |f| f << open(post['data']['url']).read }
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

def options
  Trollop.options do
    banner 'Download Wallpaper from Subreddits'
    opt :n, 'Number of images to download for each subreddit', default: 25
    opt :out, 'Directory to save wallpaper to', default: Dir.pwd
    opt :subreddits, 'Comma separated subreddits to download images from; ' \
         'the defaults are SFW', default: DEFAULT_SUBREDDITS.strip
  end
end

def main
  abort('No Internet connection available.') unless internet_connection?

  opts = options

  threads = []
  opts[:subreddits].split(',').each do |subreddit|
    threads << Thread.new do
      download_images_for_subreddit(subreddit, opts[:out])
    end
  end
  threads.each(&:join)
end

main
