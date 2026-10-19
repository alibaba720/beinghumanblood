with open('home.html', 'r', encoding='utf-8') as f:
    h = f.read()

HTML_SECTION = """<!-- INSPIRATION -->
<section class="section">
  <div class="section-head">
    <h2 class="section-title" data-i18n="inspTitle">The Philosophy of BeingHuman</h2>
    <p class="section-sub" data-i18n="inspSub">Humanity Beyond Borders</p>
  </div>
  <div class="insp-box">
    <div class="insp-icon">🌍</div>
    <div class="insp-text" data-i18n="inspText1"></div>
    <div class="insp-text" data-i18n="inspText2"></div>
    <div class="insp-text" data-i18n="inspText3"></div>
  </div>
</section>

<!-- HOW IT WORKS -->"""

CSS_SECTION = """/* INSPIRATION */
.insp-box {
  background: linear-gradient(135deg, #fffdfa, #fdf4ea);
  border: 2px solid var(--border);
  border-radius: 16px;
  padding: 30px 25px;
  text-align: center;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0,0,0,0.04);
  margin-top: 10px;
}
.insp-icon { font-size: 40px; margin-bottom: 15px; }
.insp-text {
  font-size: 15px; color: #4a3b32; line-height: 1.8;
  margin-bottom: 15px; font-weight: 500;
}
.insp-text:last-child { margin-bottom: 0; }
body.lang-urdu .insp-text { font-size: 17px; line-height: 2.4; text-align: right; }

/* HOW IT WORKS */"""

en_keys = """    inspTitle: "The Philosophy of BeingHuman",
    inspSub: "Humanity Beyond Borders",
    inspText1: "While this platform is a proud Pakistani initiative, its core inspiration stems from a powerful message of humanity presented by Salman Khan in one of his films. The philosophy is simple: Help three people, and ask them to help three more. Let kindness multiply.",
    inspText2: "We believe that for humanity, it does not matter which country you belong to — Indian, Pakistani, or from anywhere in the world. Being human is all that matters. Blood knows no borders, and true humanity means helping others without any discrimination.",
    inspText3: "This thought moved us to create a space where saving a life is the only priority. We don't seek thanks; we only seek to pass this message of humanity forward.","""

rm_keys = """    inspTitle: "BeingHuman ki Falsafa",
    inspSub: "Insaniyat ki Koi Sarhad Nahi",
    inspText1: "Ye platform ek Pakistani koshish hai, lekin iski asal inspiration Salman Khan ki ek film se aayi hai jisme unho ne insaniyat ka paigham diya. Falsafa simple hai: 3 logon ki madad karo, aur unse kaho ke wo mazeed 3 ki karein.",
    inspText2: "Hum mante hain ke insaniyat ke liye ye zaroori nahi ke aap kis mulk se hain — Indian, Pakistani, ya kahin aur se. Insan hona hi sabse ahem hai. Khoon koi sarhad nahi janta, aur asli insaniyat ka matlab hai bina kisi tafreeq ke doosron ki madad karna.",
    inspText3: "Isi soch ne humein is qabil banaya ke jahan jaan bachana sabse pehle ho. Hum shukriya nahi chahte, bas insaniyat ka ye paigham aage badhana chahte hain.","""

ur_keys = """    inspTitle: "انسانیت کی کوئی سرحد نہیں",
    inspSub: "ہمارا فلسفہ",
    inspText1: "یہ پلیٹ فارم اگرچہ ایک پاکستانی کاوش ہے، لیکن اس کی بنیاد وہ پیغام ہے جو سلمان خان نے اپنی ایک فلم میں انسانیت کے حوالے سے دیا — کہ تین لوگوں کی مدد کریں، اور ان سے کہیں کہ وہ بھی تین کی مدد کریں۔",
    inspText2: "ہمارا ماننا ہے کہ انسانیت کے لیے یہ جاننا ضروری نہیں کہ آپ کا تعلق کس ملک سے ہے — ہندوستان ہو، پاکستان ہو، یا دنیا کا کوئی بھی کونا۔ انسان ہونا ہی سب سے اہم ہے۔ خون کوئی سرحد نہیں جانتا، اور انسانیت کا مطلب ہی بلا تفریق دوسروں کی مدد کرنا ہے۔",
    inspText3: "یہی سوچ ہمیں کسی کی جان بچانے پر مجبور کرتی ہے۔ ہم کسی شکریے کے طلب گار نہیں، بس انسانیت کا یہ پیغام آگے بڑھانا چاہتے ہیں۔","""

# HTML & CSS Inject
h = h.replace('<!-- HOW IT WORKS -->', HTML_SECTION)
h = h.replace('/* HOW IT WORKS */', CSS_SECTION)

# Translations Inject
en_target = 'founderMsg: \'"I built BeingHuman Blood after seeing families struggle for a single drop of blood. Technology should serve humanity — this is my small contribution to that belief. Every drop counts. Every life matters."\','
h = h.replace(en_target, en_target + "\n" + en_keys)

rm_target = 'founderMsg: \'"Maine BeingHuman Blood banaya jab dekha ke families ek qatre khoon ke liye kitna struggle karti hain. Technology insaniyat ki khidmat kare — ye meri chhoti si koshish hai. Har qatra qeemti hai. Har zindagi qeemti hai."\','
h = h.replace(rm_target, rm_target + "\n" + rm_keys)

ur_target = 'founderMsg: \'"میں نے BeingHuman Blood اس وقت بنایا جب دیکھا کہ خاندان ایک قطرے خون کے لیے کتنی جدوجہد کرتے ہیں۔ ٹیکنالوجی انسانیت کی خدمت کرے — یہ میری چھوٹی سی کوشش ہے۔ ہر قطرہ قیمتی ہے۔ ہر زندگی قیمتی ہے۔"\','
h = h.replace(ur_target, ur_target + "\n" + ur_keys)

with open('home.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done")
