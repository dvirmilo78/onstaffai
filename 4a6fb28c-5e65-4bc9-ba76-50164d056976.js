// src/app.jsx — root composition
const { useState, useEffect } = React;

const App = () => {
  const defaults = JSON.parse(document.getElementById("tweak-defaults").textContent.replace(/\/\*EDITMODE-(BEGIN|END)\*\//g, ""));
  const [lang, setLang] = useState("he");
  const [tweaks, setTweaks] = useState(defaults);
  const [tweaksOpen, setTweaksOpen] = useState(false);

  useEffect(() => {
    document.documentElement.setAttribute("data-palette", tweaks.palette);
    document.documentElement.setAttribute("data-dark", String(tweaks.dark));
  }, [tweaks]);

  useEffect(() => {
    document.documentElement.setAttribute("lang", lang);
    document.documentElement.setAttribute("dir", lang === "he" ? "rtl" : "ltr");
  }, [lang]);

  useEffect(() => {
    const onMsg = (e) => {
      const d = e.data;
      if (!d || typeof d !== "object") return;
      if (d.type === "__activate_edit_mode") setTweaksOpen(true);
      if (d.type === "__deactivate_edit_mode") setTweaksOpen(false);
    };
    window.addEventListener("message", onMsg);
    window.parent.postMessage({ type: "__edit_mode_available" }, "*");
    return () => window.removeEventListener("message", onMsg);
  }, []);

  const L = T[lang];
  const agents = lang === "he" ? AGENTS_HE : AGENTS_EN;

  const scrollToDemo = (k) => {
    const el = document.getElementById("demo");
    if (el) el.scrollIntoView ? window.scrollTo({ top: el.offsetTop - 80, behavior: "smooth" }) : null;
  };

  return (
    <>
      <nav className="nav">
        <div className="wrap nav-inner">
          <div className="brand"><LogoMark/> OnStaffAI</div>
          <div className="nav-links">
            <a href="#agents">{L.nav.agents}</a>
            <a href="#how">{L.nav.how}</a>
            <a href="#roi">{L.nav.roi}</a>
            <a href="#demo">{L.nav.demo}</a>
            <a href="#pricing">{L.nav.pricing}</a>
          </div>
          <div className="nav-right">
            <div className="lang-toggle">
              <button className={lang === "he" ? "on" : ""} onClick={() => setLang("he")}>עב</button>
              <button className={lang === "en" ? "on" : ""} onClick={() => setLang("en")}>EN</button>
            </div>
            <a href="#pricing" className="btn btn-primary" style={{ padding: "9px 16px", fontSize: 14 }}>{L.cta.primary}</a>
          </div>
        </div>
      </nav>

      <Hero lang={lang} tHero={L.hero} tCta={L.cta} variant={tweaks.heroVariant} animKind={tweaks.heroAnim}/>
      <MetricStrip metrics={L.metrics}/>
      <AgentsGrid agents={agents} head={L.agentsHead}/>
      <HowItWorks head={L.howHead} steps={L.how}/>
      <ROI head={L.roiHead} t={L.roi} lang={lang}/>
      <LiveDemo head={L.demoHead} agents={agents} scripts={DEMO_SCRIPTS} lang={lang}/>
      <Testimonials head={L.quotesHead} quotes={L.quotes}/>
      <Pricing head={L.pricingHead} plans={L.plans}/>
      <FAQ head={L.faqHead} faq={L.faq}/>
      <CTABanner t={L.ctaBanner}/>
      <Footer t={L.footer}/>

      <TweaksPanel open={tweaksOpen} onClose={() => setTweaksOpen(false)} state={tweaks} setState={setTweaks} lang={lang}/>
    </>
  );
};

ReactDOM.createRoot(document.getElementById("root")).render(<App/>);
