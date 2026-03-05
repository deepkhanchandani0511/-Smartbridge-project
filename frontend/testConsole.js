const puppeteer = require("puppeteer");
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  page.on("console", (msg) => {
    console.log("PAGE LOG:", msg.text());
  });
  page.on("pageerror", (err) => {
    console.error("PAGE ERROR:", err.toString());
  });
  try {
    await page.goto("http://localhost:3000", {
      waitUntil: "networkidle0",
      timeout: 10000,
    });
    console.log("Loaded");
  } catch (e) {
    console.error("Goto error", e);
  }
  await browser.close();
})();
