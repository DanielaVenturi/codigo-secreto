<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import axios from "axios";

const L = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const palavras = ["BOLA", "GATO", "CASA", "BANANA", "ESCOLA", "LOGICA", "ROBO", "CODIGO", "PENSAR", "SEGREDO"];
const jaTerminou = ref(false);
const abas = computed(() => {
  const lista = [["jogo", "Jogar"], ["ranking", "Ranking"], ["tabela", "Tabela do código"]];
  if (jaTerminou.value) lista.push(["tradutor", "Tradutor"]);
  return lista;
});

const aba = ref("jogo");
const fase = ref("inicio"); // inicio | partida | fim
const nome = ref("");
const erroNome = ref("");
const i = ref(0), pts = ref(0), dicas = ref(0), erros = ref(0), secs = ref(0);
const feito = ref(false);
const resp = ref("");
const fb = ref(""), fbOk = ref(false);
const salvo = ref("");
const lista = ref([]);
const texto = ref(""), nums = ref("");
let t0 = 0, tick = null, poll = null;

const limpa = (s) => s.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toUpperCase();
const fmt = (s) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;

const palavra = computed(() => palavras[i.value]);
const numeros = computed(() => [...palavra.value].map((c) => L.indexOf(c) + 1));
const revelado = computed(() =>
  [...palavra.value].map((c, k) => (feito.value || k < dicas.value ? c : "?"))
);
const mostrarRev = computed(() => feito.value || dicas.value > 0);
const ultima = computed(() => i.value === palavras.length - 1);
const paraNum = computed(() =>
  [...limpa(texto.value)]
    .map((c) => (c === " " ? 0 : L.indexOf(c) + 1))
    .filter((n, k, a) => n > 0 || (n === 0 && k > 0 && a[k - 1] > 0))
);
const paraLetra = computed(() =>
  nums.value.split(/\s+/).filter(Boolean).map((p) => {
    const n = parseInt(p, 10);
    return n >= 1 && n <= 26 ? L[n - 1] : "?";
  })
);

function novaPalavra() {
  resp.value = ""; fb.value = ""; dicas.value = 0; erros.value = 0; feito.value = false;
}
function comecar() {
  if (!nome.value.trim()) { erroNome.value = "Escreva seu nome para começar."; return; }
  erroNome.value = ""; i.value = 0; pts.value = 0; secs.value = 0; salvo.value = "";
  novaPalavra(); fase.value = "partida"; t0 = Date.now();
  clearInterval(tick);
  tick = setInterval(() => (secs.value = Math.floor((Date.now() - t0) / 1000)), 500);
}
function conferir() {
  if (feito.value) {
    if (ultima.value) return terminar();
    i.value++; novaPalavra(); return;
  }
  const v = limpa(resp.value.trim());
  if (!v) { fbOk.value = false; fb.value = "Digite uma palavra primeiro."; return; }
  if (v === palavra.value) {
    const ganho = Math.max(1, 10 - 2 * dicas.value - erros.value);
    pts.value += ganho; feito.value = true; fbOk.value = true; fb.value = `Muito bem! +${ganho} pontos`;
  } else {
    erros.value++; fbOk.value = false; fb.value = "Ainda não. Confira a tabela e tente de novo!";
  }
}
function dica() {
  if (dicas.value < palavra.value.length - 1) dicas.value++;
}
async function terminar() {
  clearInterval(tick);
  secs.value = Math.floor((Date.now() - t0) / 1000);
  fase.value = "fim"; jaTerminou.value = true; salvo.value = "Salvando no ranking...";
  try {
    await axios.post("/api/ranking", { name: nome.value.trim(), score: pts.value, secs: secs.value });
    salvo.value = "Salvo no ranking da turma!";
    carregar();
  } catch {
    salvo.value = "Não consegui salvar no ranking. Chame o professor.";
  }
}
async function carregar() {
  try { lista.value = (await axios.get("/api/ranking")).data; } catch { /* tenta no próximo ciclo */ }
}
async function zerar() {
  const token = prompt("Senha do professor:");
  if (!token || !confirm("Apagar todo o ranking?")) return;
  try {
    await axios.delete("/api/ranking", { headers: { "X-Admin-Token": token } });
    carregar();
  } catch { alert("Senha incorreta."); }
}

onMounted(() => { carregar(); poll = setInterval(carregar, 5000); });
onUnmounted(() => { clearInterval(poll); clearInterval(tick); });
</script>

<template>
  <main>
    <h1>Código <span>Secreto</span></h1>
    <p class="sub">Cada número é uma letra: 1 = A, 2 = B, 3 = C… Descubra as palavras escondidas!</p>

    <nav>
      <button v-for="[k, t] in abas" :key="k" :class="{ on: aba === k }" @click="aba = k">{{ t }}</button>
    </nav>

    <section v-if="aba === 'jogo'" class="panel">
      <div v-if="fase === 'inicio'">
        <label for="nome">Qual é o seu nome?</label>
        <input id="nome" v-model="nome" maxlength="16" autocomplete="off" placeholder="Seu nome" @keyup.enter="comecar" />
        <p class="hint">São 10 palavras. Quem fizer mais pontos e for mais rápido sobe no ranking. Dica custa pontos!</p>
        <button class="go" @click="comecar">Começar</button>
        <p class="msg bad">{{ erroNome }}</p>
      </div>

      <div v-else-if="fase === 'partida'">
        <div class="prog">
          <span>Palavra {{ i + 1 }} de {{ palavras.length }}</span>
          <span>Pontos: {{ pts }}</span>
          <span>Tempo: {{ fmt(secs) }}</span>
        </div>
        <div class="tiles num"><div v-for="(n, k) in numeros" :key="k" class="tile">{{ n }}</div></div>
        <label for="resp">Qual é a palavra?</label>
        <input id="resp" v-model="resp" :disabled="feito" autocomplete="off" autocapitalize="characters"
          spellcheck="false" placeholder="Digite aqui" @keyup.enter="conferir" />
        <div class="row">
          <button class="go" @click="conferir">{{ feito ? (ultima ? "Terminar" : "Próxima palavra") : "Conferir" }}</button>
          <button v-if="!feito" @click="dica">Dica (−2 pontos)</button>
        </div>
        <p class="msg" :class="fbOk ? 'ok' : 'bad'">{{ fb }}</p>
        <div v-if="mostrarRev" class="tiles">
          <div v-for="(c, k) in revelado" :key="k" class="tile">{{ c }}<small v-if="c !== '?'">{{ numeros[k] }}</small></div>
        </div>
      </div>

      <div v-else>
        <p class="big">{{ pts }} pontos</p>
        <p>{{ nome }}, você terminou em {{ fmt(secs) }}!</p>
        <p class="msg">{{ salvo }}</p>
        <div class="row">
          <button class="go" @click="fase = 'inicio'">Jogar de novo</button>
          <button @click="aba = 'ranking'">Ver ranking</button>
        </div>
      </div>
    </section>

    <section v-else-if="aba === 'ranking'" class="panel">
      <ol class="rank">
        <li v-if="!lista.length">Ninguém jogou ainda. Seja o primeiro!</li>
        <li v-for="(r, n) in lista" :key="r.name">
          <span class="pos">{{ n + 1 }}º</span>
          <span class="nm">{{ r.name }}</span>
          <span class="tm">{{ fmt(r.secs) }}</span>
          <span class="pt">{{ r.score }} pts</span>
        </li>
      </ol>
      <button @click="zerar">Zerar ranking (professor)</button>
    </section>

    <section v-else-if="aba === 'tabela'" class="panel">
      <p>Use esta tabela para trocar números por letras.</p>
      <div class="grid"><div v-for="(c, k) in L" :key="c" class="tile"><b>{{ k + 1 }}</b>{{ c }}</div></div>
    </section>

    <section v-else class="panel">
      <label for="tx">Escreva uma palavra ou frase</label>
      <input id="tx" v-model="texto" placeholder="BANANA" />
      <div class="tiles num"><div v-for="(n, k) in paraNum" :key="k" class="tile" :class="{ gap: n === 0 }">{{ n || "" }}</div></div>
      <label for="nm">Ou escreva números separados por espaço</label>
      <input id="nm" v-model="nums" placeholder="2 1 14 1 14 1" />
      <div class="tiles"><div v-for="(c, k) in paraLetra" :key="k" class="tile">{{ c }}</div></div>
    </section>
  </main>
</template>

<style>
:root { --bg:#fff7d6; --ink:#1c2541; --card:#fff; --blue:#3a5bff; --pink:#ff5d8f; --green:#1fbf8f; --soft:#e9edff; }
* { box-sizing: border-box; }
body { margin:0; background:var(--bg); color:var(--ink); font-family:"Baloo 2","Trebuchet MS",system-ui,sans-serif; font-size:20px; line-height:1.35; }
main { max-width:860px; margin:0 auto; padding:20px 16px 48px; }
h1 { font-size:clamp(2rem,7vw,3.4rem); margin:8px 0 4px; font-weight:800; line-height:1.05; }
h1 span { color:var(--pink); }
.sub { margin:0 0 18px; opacity:.85; }
nav { display:flex; gap:8px; flex-wrap:wrap; margin-bottom:18px; }
button { font:inherit; font-weight:700; border:3px solid var(--ink); background:var(--card); color:var(--ink); border-radius:14px; padding:6px 16px; cursor:pointer; box-shadow:0 4px 0 var(--ink); }
button:active { transform:translateY(3px); box-shadow:0 1px 0 var(--ink); }
button.on { background:var(--blue); color:#fff; }
button.go { background:var(--green); color:#0b2a20; }
:focus-visible { outline:4px solid var(--pink); outline-offset:2px; }
.panel { background:var(--card); border:3px solid var(--ink); border-radius:22px; padding:18px; box-shadow:0 6px 0 var(--ink); }
.tiles { display:flex; flex-wrap:wrap; gap:10px; margin:14px 0; }
.tile { min-width:64px; text-align:center; background:var(--soft); border:3px solid var(--ink); border-radius:14px; padding:4px 10px; font-weight:800; font-size:2.2rem; }
.tile small { display:block; font-size:.8rem; opacity:.7; font-weight:500; }
.tile.gap { background:transparent !important; border:0; min-width:24px; }
.tiles.num .tile { background:var(--blue); color:#fff; }
input { font:inherit; font-size:1.6rem; font-weight:700; width:100%; border:3px solid var(--ink); border-radius:14px; padding:8px 14px; background:var(--card); color:var(--ink); text-transform:uppercase; }
label { font-weight:700; display:block; margin:12px 0 6px; }
.row { display:flex; gap:10px; flex-wrap:wrap; margin-top:12px; }
.msg { font-weight:800; min-height:1.5em; margin:10px 0 0; }
.ok { color:var(--green); } .bad { color:var(--pink); }
.prog { display:flex; justify-content:space-between; gap:8px; flex-wrap:wrap; font-weight:700; opacity:.85; }
.hint { font-size:.9rem; opacity:.8; }
.big { font-size:3rem; font-weight:800; color:var(--pink); margin:0; }
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(74px,1fr)); gap:10px; }
.grid .tile { min-width:0; padding:4px; }
.grid .tile b { display:block; font-size:1rem; color:var(--blue); }
ol.rank { list-style:none; margin:0 0 14px; padding:0; }
ol.rank li { display:flex; gap:12px; align-items:center; padding:8px 12px; border:3px solid var(--ink); border-radius:14px; margin-bottom:8px; background:var(--soft); font-weight:700; }
ol.rank li:first-child { background:#ffd54a; }
.pos { font-size:1.6rem; min-width:2.2ch; } .nm { flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; } .tm { font-size:.85rem; opacity:.75; }
</style>
