<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
  <div class="center-text">
    <h1 align="center">
    	🕷️ Arachnida 🕷️
    </h1>
    <h3 align="center">
      <i>
    	  Introductory project to web scraping and metadata.
      </i>
    </h3>
    <div align="center">
      <img alt="42" src="https://i.imgur.com/FBTPTt0.png" width="300px"/>
    </div>
  </div>
  <h2>Spider Program</h2>
  <p>
    The spider program allows you to extract images from a website.
  </p>
  <p>Usage:</p>
  <pre>
    <code>./spider [-rlp] URL</code>
  </pre>
  <ul>
    <li><strong>-r:</strong> Recursively download images from the provided URL.</li>
    <li><strong>-r -l [N]:</strong> Set maximum depth level for recursive download (default: 5).</li>
    <li><strong>-p [PATH]:</strong> Set path for downloaded files (default: ./data/).</li>
  </ul>
  <p>Default file extensions downloaded:</p>
  <ul>
    <li>.jpg/jpeg</li>
    <li>.png</li>
    <li>.gif</li>
    <li>.bmp</li>
  </ul>

  <h2>Scorpion Program</h2>
  <p>The scorpion program parses image files for EXIF and other metadata.</p>
  <p>Usage:</p>
  <pre>
    <code>./scorpion FILE1 [FILE2 ...]</code>
  </pre>
  <p>Basic attributes displayed:</p>
  <ul>
    <li>Creation date</li>
    <li>EXIF data</li>
  </ul>

  <h2>What is EXIF (Exchangeable image file format)</h2>
  <p>It's a standard that specifies information added to images and sound used by cameras, scanners and other systems that handle this type of data.</p>
  <p>It covers a broad spectrum of information such as:</p>
  <li>Camera Settings</li>
  <li>Image metrics</li>
  <li>Date and time information</li>
  <li>Location information</li>
  <li>Descriptions</li>
  <li>Copyright information</li>

  <h2>Why is EXIF relevant?</h2>
  <p>Since the Exif tag contains metadata about the photo, it can pose a privacy problem.</p>
  <p>For example users are usually unaware that when a photo is shared it may potentially reveal the exact location and time it was taken and this is all done by default.</p>
  <p>The privacy problem of Exif data can be avoided by removing the Exif data using a metadata removal tool.</p>

  <h2>Implementation Details</h2>
  <p>Both programs must be developed without using wget or scrapy.</p>
  <p>Functions or libraries for HTTP requests and file handling are allowed. The rest is forbidden.</p>

  <h2>License</h2>
  <p>This project is licensed under the MIT License - see the <a href="LICENSE">LICENSE</a> file for details.</p>
</body>
</html>
