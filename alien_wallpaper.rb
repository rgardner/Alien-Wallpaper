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


def ignore_post?(post)
  return true if post.nil?
  return true if post['data']['is_self']

  unless post['data']['url'].match(FILE_EXTENSION_REGEX)
    $stderr.puts post['data']['url']
    return true
  end
end

# Download the image associated with the Reddit post.
def download_image(post, output_dir)
  return if ignore_post?(post)

  # Construct the filename and filepath
  filename = post['data']['id'] +
             post['data']['url'].match(FILE_EXTENSION_REGEX)[0]
  filepath = File.join(output_dir, filename)
  puts filepath

  # Need to use write-binary (wb) mode for images
  File.open(filepath, 'wb') do |f|
    f << open(post['data']['url']).read
  end
end

def get_opts
  Trollop.options do
    banner 'Download Wallpaper from Subreddits'
    opt :n, 'Number of images to download for each subreddit', default: 25
    opt :out, 'Directory to save wallpaper to', default: Dir.pwd
    opt :subreddits, 'Comma separated subreddits to download images from; ' \
         'the defaults are SFW', default: DEFAULT_SUBREDDITS.strip
  end
end

def main
  opts = get_opts

  opts[:subreddits].split(',').each do |subreddit|
    url = "http://www.reddit.com/r/#{subreddit}.json"
    res = Net::HTTP.get(URI(url))
    json = JSON.parse(res)
    json['data']['children'].each do |post|
      download_image(post, opts[:out])
    end
  end
end

main
