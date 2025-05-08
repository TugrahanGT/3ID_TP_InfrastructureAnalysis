// components.js

const navbarHTML = `
  <nav class="navbar">
    <div class="nav-container">
      <span class="logo">Triple-ID</span>
      <ul class="nav-links">
        <li><a href="/">System Status</a></li>
        <li><a href="/informative">NIST Compliance Rules</a></li>
        <li><a href="/about">About Us</a></li>
      </ul>
    </div>
  </nav>
`;

document.getElementById('navbar-placeholder').innerHTML = navbarHTML;

const footerHTML = `
<footer class="footer">
<div class="footer-content">
  <!-- Left: Company Info -->
  <div>
    <h3>Triple-ID</h3>
    <p>Innovating secure systems through modern compliance and intelligent infrastructure design.</p>
  </div>

  <!-- Middle: Quick Links -->
  <div>
    <h4>Quick Links</h4>
    <ul style="list-style: none; padding: 0;">
      <li><a href="/">System Status</a></li>
      <li><a href="/informative">NIST Compliance Rules</a></li>
      <li><a href="/about">About Us</a></li>
    </ul>
  </div>

  <!-- Right: Contact Form -->
  <div>
    <h4>Contact Us</h4>
    <form>
      <input type="email" placeholder="Your Email" required>
      <textarea placeholder="Your Message" required></textarea>
      <button type="submit">Send</button>
    </form>
  </div>
</div>
</footer>
`;

document.getElementById('footer-placeholder').innerHTML = footerHTML;