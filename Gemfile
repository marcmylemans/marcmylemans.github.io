# frozen_string_literal: true

source "https://rubygems.org"

gem "jekyll-theme-chirpy", "~> 6.5", ">= 6.5.5"

group :test do
  gem "html-proofer", "~> 4.4"
end

# Windows and JRuby does not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library.
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

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]

# Lock `http_parser.rb` gem to `v0.6.x` on JRuby builds since newer versions of the gem
# do not have a Java counterpart.
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]
