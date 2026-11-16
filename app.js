const $ = (id) => document.getElementById(id);
const pick = (items) => items[Math.floor(Math.random() * items.length)];
const output = $('mainOutput');
const meta = $('outputMeta');
const stamp = $('outputTime');

function show(message, tag = 'RANDOM OUTPUT') {
  output.textContent = message;
  meta.textContent = 'READY // ' + tag + ' // LOCAL ONLY';
  stamp.textContent = new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
}

const chaos = [
  'A tiny wizard has been hired to manage the printer. Nobody knows who hired him.',
  'New invention: a toaster that only toasts bread when you say something encouraging.',
  'The moon has submitted a support ticket. Priority: medium.',
  'Somewhere, a Roomba is learning ancient forbidden geometry.',
  'A duck in a tiny hard hat is now in charge of the internet.',
  'You found a button labelled DO NOT PRESS. It has a little party hat.',
  'A committee of raccoons has approved your proposal. They request snacks.',
  'Breaking: local potato achieves sentience, immediately asks for a vacation.',
  'The simulation has detected excessive silliness. Increasing silliness.',
  'A mysterious door appears. It leads to a slightly smaller door.'
];

function startup() {
  const names = ['GoblinCloud','ToastStack','MoonBucket','SockOS','Crumbly','DuckWare','DefinitelyReal'];
  const products = ['AI-powered sandwich forecasting','blockchain-powered houseplants','subscription-based cloud rocks','on-demand kazoo logistics','automated sock matching','virtual reality for pigeons'];
  const pitches = ['We disrupt the concept of having a normal Tuesday.','We put the cloud in a jar. The jar is extra.','Our technology is 90% stickers and 10% optimism.','We are solving a problem that we invented yesterday.'];
  const funding = ['$4.2 million and one suspicious coupon','$800 and a very supportive aunt','three shiny buttons and a paperclip','one billion imaginary dollars'];
  show(pick(names) + ' Inc.\n' + pick(products) + '. ' + pick(pitches) + '\nFunding goal: ' + pick(funding) + '.', 'STARTUP GENERATED');
}

function nameMachine() {
  const a = ['Zorp','Bingle','Mox','Quibble','Noodle','Vex','Plinko','Gizmo','Wobble','Crank'];
  const b = ['tron','berry','opolis','ington','spark','blob','zilla','byte','whistle','beep'];
  const labels = ['ROBOT DESIGNATION','PLANET NAME','SNACK BRAND','MYSTERIOUS CREATURE'];
  show(pick(a) + pick(b) + ' — ' + pick(labels), 'NAME FORGED');
}

function oracle() {
  const question = $('question').value.trim();
  if (!question) { show('The oracle requires a question. It is tiny, not psychic.', 'ORACLE NEEDS INPUT'); return; }
  const answers = ['Absolutely. But bring snacks.','The signs point to maybe.','Ask again after the next biscuit.','No. The council of spoons has spoken.','Yes, but only on Tuesdays.','The answer is hidden inside a suspiciously normal sandwich.','Probably. Consult a qualified wizard first.','The oracle says: make a tiny prototype and see what happens.'];
  show('Q: ' + question + '\n\nA: ' + pick(answers), 'TINY ORACLE');
  $('question').value = '';
}

$('chaosBtn').addEventListener('click', () => show(pick(chaos), 'CHAOS GENERATED'));
document.querySelector('[data-tool="startup"]').addEventListener('click', startup);
document.querySelector('[data-tool="name"]').addEventListener('click', nameMachine);
$('askBtn').addEventListener('click', oracle);
$('question').addEventListener('keydown', e => { if (e.key === 'Enter') oracle(); });
$('glitchBtn').addEventListener('click', () => {
  document.body.classList.remove('glitch');
  void document.body.offsetWidth;
  document.body.classList.add('glitch');
  show('WARNING: reality.exe has stopped responding.\nJust kidding. Everything is fine. Probably.', 'VISUAL TEST');
  setTimeout(() => document.body.classList.remove('glitch'), 1500);
});
