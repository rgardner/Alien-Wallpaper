#!/usr/bin/env ruby

# Name: alien_wallpaper.rb
# Description: Downloads top images from specified subreddits.
# Author: Bob Gardner
# Updated: 4/18/16
# License: MIT

require 'json'
require 'net/http'
require 'open-uri'
require 'optparse'

# Number of images to download per subreddit/multireddit.
NUM_IMAGES = 25

# The default subreddits to download images from.
DEFAULT_SUBREDDITS = ['ArchitecturePorn',
                      'CityPorn',
                      'EarthPorn',
                      'SkyPorn',
                      'spaceporn',
                      'winterporn',
                      'quoteporn']

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
rescue SocketError
    abort('No Internet connection available')
rescue OpenURI::HTTPError => error
    $stderr.puts error
rescue OpenSSL::SSL::SSLError => error
    $stderr.puts error
end

# Return the json representation of `subreddit`
def fetch_subreddit_data(url, count = 25, after = '')
  params = "count=#{count}&after=#{after}"
  JSON.parse(URI.parse("#{url}.json?#{params}").read)
rescue SocketError
  abort('No Internet connection available')
end

# Download `n` images from `url` to `out_dir`
def download_images_for_url(url, n, out_dir)
  json = fetch_subreddit_data(url)
  images_remaining = n
  catch(:done) do
    loop do
      json['data']['children'].each do |post|
        throw :done if images_remaining <= 0
        download_image(post, out_dir) unless ignore_post?(post)
        images_remaining -= 1
      end
      json = fetch_subreddit_data(url, json['data']['after'])
    end
  end
end

def multi_to_url(multi)
  user, multi = multi.split('/')
  "https://www.reddit.com/user/#{user}/m/#{multi}"
end

def subreddit_to_url(subreddit)
  "https://www.reddit.com/r/#{subreddit}"
end

# The command line options.
def cli_options
  options = { out: Dir.pwd, s: DEFAULT_SUBREDDITS }
  OptionParser.new do |opts|
    opts.on('--subreddits=x,y,z', Array, 'List of subreddits') do |s|
      options[:s] = s
    end
    opts.on('--multi M', String, 'user/multireddit') do |m|
      options[:m] = m
    end
    opts.on('--out DIR', String, 'Directory to save wallpaper to') do |out|
      options[:out] = out
    end
    opts.on_tail('-h', '--help', 'Show this message') do
      puts 'Download beautiful wallpaper from subreddits'
      puts opts
      exit
    end
  end.parse!
  options
end

def main(opts)
  threads = []
  urls = opts[:s].map { |s| subreddit_to_url(s) }
  urls << multi_to_url(opts[:m]) unless opts[:m].nil?
  urls.each do |url|
    threads << Thread.new do
      download_images_for_url(url, NUM_IMAGES, opts[:out])
    end
  end
  threads.each(&:join)
end

main(cli_options)
