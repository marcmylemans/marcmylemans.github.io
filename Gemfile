# frozen_string_literal: true

source "https://rubygems.org"

gemspec

gem "html-proofer", "~> 5.0", group: :test

platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

group :jekyll_plugins do
  gem "jekyll-youtube"
  gem "jekyll-include-cache"
  gem 'jekyll-seo-tag'
  gem 'jekyll-sitemap'
  gem 'jekyll-gzip'
  gem 'jekyll-analytics'
  gem 'jekyll-redirect-from'
end

gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]
