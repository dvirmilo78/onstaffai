// src/tweaks.jsx — tweak panel
const TweaksPanel = ({ open, onClose, state, setState, lang }) => {
  if (!open) return null;
  const update = (patch) => {
    const next = { ...state, ...patch };
    setState(next);
    window.parent.postMessage({ type: "__edit_mode_set_keys", edits: patch }, "*");
  };
  const palettes = [
    { k: "warm", label: lang === "he" ? "חם (כתום)" : "Warm" },
    { k: "electric", label: lang === "he" ? "אלקטרי (סגול)" : "Electric" },
    { k: "lime", label: lang === "he" ? "ליים (כהה)" : "Lime" },
  ];
  const anims = [
    { k: "flow", label: lang === "he" ? "זרימה" : "Flow" },
    { k: "charts", label: lang === "he" ? "נתונים" : "Charts" },
    { k: "orbit", label: lang === "he" ? "מסלול" : "Orbit" },
  ];
  return (
    <div className="tweaks-panel">
      <button className="tweaks-close" onClick={onClose}>×</button>
      <h5>{lang === "he" ? "שיפוצים" : "Tweaks"}</h5>

      <div style={{ fontSize: 12, color: "var(--mute)", marginBottom: 6, fontWeight: 600 }}>{lang === "he" ? "פלטה" : "Palette"}</div>
      <div className="row">
        {palettes.map(p => (
          <button key={p.k} className={"chip" + (state.palette === p.k ? " on" : "")} onClick={() => update({ palette: p.k, dark: p.k === "lime" })}>{p.label}</button>
        ))}
      </div>

      <div style={{ fontSize: 12, color: "var(--mute)", marginBottom: 6, fontWeight: 600 }}>{lang === "he" ? "מצב" : "Mode"}</div>
      <div className="row">
        <button className={"chip" + (!state.dark ? " on" : "")} onClick={() => update({ dark: false })}>{lang === "he" ? "בהיר" : "Light"}</button>
        <button className={"chip" + (state.dark ? " on" : "")} onClick={() => update({ dark: true })}>{lang === "he" ? "כהה" : "Dark"}</button>
      </div>

      <div style={{ fontSize: 12, color: "var(--mute)", marginBottom: 6, fontWeight: 600 }}>{lang === "he" ? "כותרת Hero" : "Hero headline"}</div>
      <div className="row">
        {[0,1,2].map(i => (
          <button key={i} className={"chip" + (state.heroVariant === i ? " on" : "")} onClick={() => update({ heroVariant: i })}>v{i+1}</button>
        ))}
      </div>

      <div style={{ fontSize: 12, color: "var(--mute)", marginBottom: 6, fontWeight: 600 }}>{lang === "he" ? "אנימציית וידאו" : "Video anim"}</div>
      <div className="row" style={{ marginBottom: 0 }}>
        {anims.map(a => (
          <button key={a.k} className={"chip" + (state.heroAnim === a.k ? " on" : "")} onClick={() => update({ heroAnim: a.k })}>{a.label}</button>
        ))}
      </div>
    </div>
  );
};

Object.assign(window, { TweaksPanel });
