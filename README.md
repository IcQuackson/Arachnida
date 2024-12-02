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

  <h3>Bonus Features</h3>
  <ul>
    <li>Option to modify/delete metadata in the scorpion program.</li>
    <li>Graphical interface for viewing and managing metadata.</li>
  </ul>

  <h2>Implementation Details</h2>
  <p>Both programs must be developed without using wget or scrapy.</p>
  <p>Functions or libraries for HTTP requests and file handling are allowed. The rest is forbidden.</p>

  <h2>License</h2>
  <p>This project is licensed under the MIT License - see the <a href="LICENSE">LICENSE</a> file for details.</p>
</body>
</html>
