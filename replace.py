import re

with open('/Users/sev/Projects/FloppyLetters/FloppyLetter2601/block.txt', 'r') as f:
    text = f.read()

# We will manually construct VERB_REGISTRY by processing `text`.
# It's safer to just do a python script that writes out the exact replacement text manually.

registry_code = """
const VERB_REGISTRY = [
  // ── Multi-word pattern dispatch ──────────────────────────────────────────
  { test: (cmd, args, rest) => cmd === 'look'  && args[0] === 'at', exec: (cmd, args, rest) => { gameExamine(args.slice(1)); } },
  { test: (cmd, args, rest) => cmd === 'look'  && /^around/.test(rest), exec: (cmd, args, rest) => { gameLook(); } },
  { test: (cmd, args, rest) => cmd === 'look'  && /^(out|outside|through)/.test(rest), exec: (cmd, args, rest) => { gameExamine(['window']); } },
  { test: (cmd, args, rest) => cmd === 'look'  && (args[0] === 'in' || args[0] === 'inside' || args[0] === 'into'), exec: (cmd, args, rest) => { gameExamine(args.slice(1)); } },
  { test: (cmd, args, rest) => cmd === 'where' && /^am\\b/.test(rest), exec: (cmd, args, rest) => { handleGameCommand('where'); } },
  { test: (cmd, args, rest) => cmd === 'pick'  && args[0] === 'up', exec: (cmd, args, rest) => { gameTake(args.slice(1)); } },
  { test: (cmd, args, rest) => cmd === 'put'   && args[0] === 'down', exec: (cmd, args, rest) => { gameDrop(args.slice(1)); } },
  { test: (cmd, args, rest) => cmd === 'put'   && /on (the )?turntable/.test(rest), exec: (cmd, args, rest) => { gamePlay(rest.replace(/\\s*on (the )?turntable/, '').trim().split(' ')); } },
  { test: (cmd, args, rest) => cmd === 'turn'  && args[0] === 'on'  && /coffee|maker|coffeemaker/.test(args.slice(1).join(' ')), exec: (cmd, args, rest) => { gameStartBrew(); } },
  { test: (cmd, args, rest) => cmd === 'turn'  && args[0] === 'off' && /coffee|maker|coffeemaker/.test(args.slice(1).join(' ')), exec: (cmd, args, rest) => { addLine(GameState.coffeePotState === 'brewing' ? "It's already going. Let it finish." : "The coffee maker is off."); } },
  { test: (cmd, args, rest) => cmd === 'turn'  && args[0] === 'on', exec: (cmd, args, rest) => { gameToggle(args.slice(1), true); } },
  { test: (cmd, args, rest) => cmd === 'turn'  && args[0] === 'off', exec: (cmd, args, rest) => { gameToggle(args.slice(1), false); } },
  { test: (cmd, args, rest) => cmd === 'turn'  && args[args.length - 1] === 'on', exec: (cmd, args, rest) => { gameToggle(args.slice(0, -1), true); } },
  { test: (cmd, args, rest) => cmd === 'turn'  && args[args.length - 1] === 'off', exec: (cmd, args, rest) => { gameToggle(args.slice(0, -1), false); } },
  { test: (cmd, args, rest) => cmd === 'get'   && args[0] === 'up', exec: (cmd, args, rest) => { gameStand(); } },
  { test: (cmd, args, rest) => cmd === 'stand' && args[0] === 'up', exec: (cmd, args, rest) => { gameStand(); } },
  { test: (cmd, args, rest) => cmd === 'lie'   && /^(down|on)/.test(rest), exec: (cmd, args, rest) => { gameSit(args); } },
  { test: (cmd, args, rest) => cmd === 'lay'   && /^(down|on)/.test(rest), exec: (cmd, args, rest) => { gameSit(args); } },
  { test: (cmd, args, rest) => cmd === 'go'    && (args[0] === 'to' || args[0] === 'into' || args[0] === 'in'), exec: (cmd, args, rest) => { gameGo(args.slice(1)); } },
  { test: (cmd, args, rest) => cmd === 'walk'  && (args[0] === 'to' || args[0] === 'into'), exec: (cmd, args, rest) => { gameGo(args.slice(1)); } },
  { test: (cmd, args, rest) => cmd === 'head'  && (args[0] === 'to' || args[0] === 'towards'), exec: (cmd, args, rest) => { gameGo(args.slice(1)); } },
  { test: (cmd, args, rest) => cmd === 'play'   && /message|messages|voicemail/.test(rest), exec: (cmd, args, rest) => { gamePlayMessage(); } },
  { test: (cmd, args, rest) => cmd === 'check'  && /message|messages|voicemail|machine/.test(rest), exec: (cmd, args, rest) => { gamePlayMessage(); } },
  { test: (cmd, args, rest) => cmd === 'listen' && /message|messages|voicemail|machine/.test(rest), exec: (cmd, args, rest) => { gamePlayMessage(); } },
  { test: (cmd, args, rest) => cmd === 'press'  && /play/.test(rest), exec: (cmd, args, rest) => { gamePlayMessage(); } },
  { test: (cmd, args, rest) => cmd === 'pick'   && /phone|up the phone/.test(rest), exec: (cmd, args, rest) => { addLine('You pick up the receiver. Dial tone.'); } },
  { test: (cmd, args, rest) => cmd === 'hang'   && /up/.test(rest), exec: (cmd, args, rest) => { addLine('You set the receiver back down.'); } },
  { test: (cmd, args, rest) => (cmd === 'insert' || cmd === 'load') && /vhs|video/.test(rest), exec: (cmd, args, rest) => { gameInsertVHS(); } },
  { test: (cmd, args, rest) => (cmd === 'insert' || cmd === 'load') && /cassette/.test(rest), exec: (cmd, args, rest) => { gameInsertCassette(); } },
  { test: (cmd, args, rest) => (cmd === 'insert' || cmd === 'load') && /tape/.test(rest), exec: (cmd, args, rest) => {
    if      (ITEMS.some(i => i.shelvedVHS  && GameState.gInventory.includes(i.id)))                                  gameInsertVHS();
    else if (ITEMS.some(i => i.shelvedTape && GameState.gInventory.includes(i.id) && GameState.cassettePlaying !== i.label))   gameInsertCassette();
    else                                                                                                    gameInsertFloppy();
  } },
  { test: (cmd, args, rest) => cmd === 'insert' && /floppy|disk/.test(rest), exec: (cmd, args, rest) => { gameInsertFloppy(); } },
  { test: (cmd, args, rest) => cmd === 'eject'  && /floppy|disk/.test(rest), exec: (cmd, args, rest) => { gameEjectFloppy(); } },
  { test: (cmd, args, rest) => cmd === 'remove' && /floppy|disk/.test(rest), exec: (cmd, args, rest) => { gameEjectFloppy(); } },
  { test: (cmd, args, rest) => (cmd === 'eject' || cmd === 'remove') && /cassette|boombox/.test(rest), exec: (cmd, args, rest) => { gameEjectCassette(); } },
  { test: (cmd, args, rest) => (cmd === 'eject' || cmd === 'remove') && /vhs|vcr|video|movie|tape/.test(rest), exec: (cmd, args, rest) => { gameEjectVHS(); } },
  { test: (cmd, args, rest) => cmd === 'put'    && /floppy|disk/.test(rest) && /computer|drive|slot/.test(rest), exec: (cmd, args, rest) => { gameInsertFloppy(); } },
  { test: (cmd, args, rest) => cmd === 'put'    && /vhs|tape|video|movie/.test(rest) && /vcr|player/.test(rest), exec: (cmd, args, rest) => { gamePlay(rest.replace(/\\s*(in(to)?|the)\\s*(vcr|player)/g, '').trim().split(' ')); } },
  { test: (cmd, args, rest) => cmd === 'dir'    && /floppy|disk/.test(rest), exec: (cmd, args, rest) => { GameState.floppyInserted ? (addLine(''), addLine('A:\\\\'), addLine('  LETTER  TXT     2048  10-03-93  11:48p')) : addLine("There's no disk in the drive."); } },
  { test: (cmd, args, rest) => cmd === 'type'   && /letter|txt/.test(rest), exec: (cmd, args, rest) => { gameRead(['letter.txt']); } },
  { test: (cmd, args, rest) => cmd === 'listen' && args[0] === 'to', exec: (cmd, args, rest) => { gameListen(args.slice(1)); } },
  { test: (cmd, args, rest) => cmd === 'stop'  && /record|music|player|turntable|needle/.test(rest), exec: (cmd, args, rest) => { gameStop(args); } },
  { test: (cmd, args, rest) => cmd === 'stop'  && /vcr|vhs|movie|film|video/.test(rest), exec: (cmd, args, rest) => { gameStop(args); } },
  { test: (cmd, args, rest) => cmd === 'watch' && /vcr|vhs|movie|film|video/.test(rest), exec: (cmd, args, rest) => { gameWatch(args); } },
  { test: (cmd, args, rest) => cmd === 'lift'  && /needle/.test(rest), exec: (cmd, args, rest) => { gameStop(['needle']); } },
  { test: (cmd, args, rest) => /^(pour|add|mix|put|splash)$/.test(cmd) && /half.*(half|&)|creamer|cream/.test(rest), exec: (cmd, args, rest) => { gameAddHalfAndHalf(); } },
  { test: (cmd, args, rest) => /^(pour|add|mix|splash)$/.test(cmd) && /^(in(to)?|to)\\s+(the\\s+)?(mug|cup|coffee)/.test(rest) && GameState.gInventory.includes('half and half'), exec: (cmd, args, rest) => { gameAddHalfAndHalf(); } },
  { test: (cmd, args, rest) => (cmd === 'fill' || cmd === 'pour') && /mug|cup/.test(rest), exec: (cmd, args, rest) => { gameFillMug(); } },
  { test: (cmd, args, rest) => (cmd === 'fill' || cmd === 'pour') && /glass|water/.test(rest), exec: (cmd, args, rest) => { gameFillGlass(); } },
  { test: (cmd, args, rest) => cmd === 'get'   && /water/.test(rest), exec: (cmd, args, rest) => { gameFillGlass(); } },
  { test: (cmd, args, rest) => cmd === 'pour'  && /coffee/.test(rest) && !GameState.gInventory.includes('half and half'), exec: (cmd, args, rest) => {
    if (GameState.mugFilled && (GameState.coffeePotState === 'old' || GameState.coffeePotState === 'fresh')) {
      addLine("Your mug is already full.");
      addLine("To start a fresh pot, dump the carafe first.", 'dim');
    } else { gameFillMug(); }
  } },
  { test: (cmd, args, rest) => cmd === 'get'   && /coffee/.test(rest), exec: (cmd, args, rest) => { gameFillMug(); } },
  { test: (cmd, args, rest) => cmd === 'drink' && /water|glass/.test(rest), exec: (cmd, args, rest) => { gameDrink(['water']); } },
  // ── Fresh coffee steps ───────────────────────────────────────────────────
  { test: (cmd, args, rest) => cmd === 'make' && /coffee|pot|fresh|cup/.test(rest), exec: (cmd, args, rest) => {
    if      (GameState.coffeePotState === 'old' || GameState.coffeePotState === 'fresh')
      addLine('Start by dumping the old pot.');
    else if (GameState.coffeePotState === 'empty')
      addLine('Fill the carafe from the faucet.');
    else if (GameState.coffeePotState === 'water')
      addLine(GameState.gInventory.includes('filter') ? 'Add the filter to the basket.' : 'Take a filter from the box on the counter.');
    else if (GameState.coffeePotState === 'filter')
      addLine('Scoop in the grounds.');
    else if (GameState.coffeePotState === 'grounds')
      addLine('Start the maker.');
    else if (GameState.coffeePotState === 'brewing')
      addLine("It's already going.");
  } },
  { test: (cmd, args, rest) => cmd === 'throw' && args[0] === 'away', exec: (cmd, args, rest) => { gameThrowAway(args.slice(1)); } },
  { test: (cmd, args, rest) => cmd === 'throw' && /trash|garbage|bin|away|out/.test(rest), exec: (cmd, args, rest) => { gameThrowAway(args); } },
  { test: (cmd, args, rest) => (cmd === 'toss' || cmd === 'discard') && rest, exec: (cmd, args, rest) => { gameThrowAway(args); } },
  { test: (cmd, args, rest) => (cmd === 'wash' || cmd === 'clean') && /dish|dishes|plate|plates/.test(rest), exec: (cmd, args, rest) => { addLine('You run the water and wash the few dishes in the sink. They can air dry.'); } },
  { test: (cmd, args, rest) => (cmd === 'dump' || cmd === 'empty') && /mug|cup/.test(rest), exec: (cmd, args, rest) => { gameDumpMug(); } },
  { test: (cmd, args, rest) => cmd === 'pour' && /out/.test(rest) && /mug|cup/.test(rest), exec: (cmd, args, rest) => { gameDumpMug(); } },
  { test: (cmd, args, rest) => (cmd === 'pour' || cmd === 'dump' || cmd === 'empty' || cmd === 'discard') && /coffee|pot|carafe|old/.test(rest), exec: (cmd, args, rest) => { gamePourOutCoffee(); } },
  { test: (cmd, args, rest) => cmd === 'fill' && /carafe|pot|reservoir|maker|coffee maker/.test(rest), exec: (cmd, args, rest) => { gameFillCarafe(); } },
  { test: (cmd, args, rest) => cmd === 'fill' && /water/.test(rest) && /carafe|pot|reservoir/.test(rest), exec: (cmd, args, rest) => { gameFillCarafe(); } },
  { test: (cmd, args, rest) => (cmd === 'add' || cmd === 'put' || cmd === 'place' || cmd === 'insert') && /filter/.test(rest) && /basket|maker|coffee|pot/.test(rest), exec: (cmd, args, rest) => { gameAddFilter(); } },
  { test: (cmd, args, rest) => (cmd === 'add' || cmd === 'put' || cmd === 'place') && /filter/.test(rest) && !rest.includes('box'), exec: (cmd, args, rest) => { gameAddFilter(); } },
  { test: (cmd, args, rest) => (cmd === 'add' || cmd === 'put' || cmd === 'scoop' || cmd === 'measure') && /ground|coffee|grounds/.test(rest), exec: (cmd, args, rest) => { gameAddGrounds(); } },
  { test: (cmd, args, rest) => (cmd === 'start' || cmd === 'brew' || cmd === 'run' || cmd === 'switch') && /coffee|brew|maker|pot/.test(rest), exec: (cmd, args, rest) => { gameStartBrew(); } },
  { test: (cmd, args, rest) => cmd === 'flip' && /switch|maker|coffee/.test(rest), exec: (cmd, args, rest) => { gameStartBrew(); } },
  { test: (cmd, args, rest) => cmd === 'brew' && !rest, exec: (cmd, args, rest) => { gameStartBrew(); } },
  { test: (cmd, args, rest) => cmd === 'check' && /coffee|brew|pot|carafe|maker/.test(rest), exec: (cmd, args, rest) => { checkBrew(); } },
  // ── TV channel / input switching ────────────────────────────────────────
  { test: (cmd, args, rest) => cmd === 'channel' || (cmd === 'switch' && /channel|input|vcr|aux/.test(rest)) || (cmd === 'tune'   && /channel|vcr|aux/.test(rest)), exec: (cmd, args, rest) => {
    if (!GameState.tvOn) { addLine("The TV is off."); }
    else if (GameState.vhsPlaying) addLine(`The VCR is already coming through. ${cap(GameState.vhsPlaying)} is on screen.`);
    else if (GameState.vcrOn)      addLine("The VCR is wired into channel 3. Turn it on and load a tape to watch.");
    else                 addLine("The VCR is wired into channel 3. Turn on the VCR first.");
  } },
  // ── Scrapple / cooking ───────────────────────────────────────────────────
  { test: (cmd, args, rest) => (cmd === 'put' || cmd === 'add' || cmd === 'place' || cmd === 'slice' || cmd === 'cut') && /scrapple/.test(rest) && /pan|stove|skillet/.test(rest), exec: (cmd, args, rest) => { gamePutInPan([]); } },
  { test: (cmd, args, rest) => cmd === 'slice' && /scrapple/.test(rest), exec: (cmd, args, rest) => { gamePutInPan([]); } },
  { test: (cmd, args, rest) => cmd === 'cut'   && /scrapple/.test(rest), exec: (cmd, args, rest) => { gamePutInPan([]); } },
  { test: (cmd, args, rest) => cmd === 'open'  && /kitchen drawer|knife drawer|drawer by|silverware|utensil/.test(rest), exec: (cmd, args, rest) => { gameOpen(['kitchen drawer']); } },
  { test: (cmd, args, rest) => cmd === 'close' && /kitchen drawer|knife drawer|drawer by|silverware|utensil/.test(rest), exec: (cmd, args, rest) => { gameClose(['kitchen drawer']); } },
  { test: (cmd, args, rest) => cmd === 'light' && /stove|burner|range|oven/.test(rest), exec: (cmd, args, rest) => { gameToggle(['stove'], true); } },
  { test: (cmd, args, rest) => cmd === 'ignite'&& /stove|burner|range/.test(rest), exec: (cmd, args, rest) => { gameToggle(['stove'], true); } },
  { test: (cmd, args, rest) => cmd === 'fry'   && /scrapple|breakfast|it/.test(rest), exec: (cmd, args, rest) => { gameCook(['scrapple']); } },
  { test: (cmd, args, rest) => cmd === 'fry'   && !rest, exec: (cmd, args, rest) => { gameCook([]); } },
  { test: (cmd, args, rest) => cmd === 'watch' && /tv|television|set|show|hogan|screen/.test(rest), exec: (cmd, args, rest) => { gameWatch(args); } },
  
  // ── Switch cases ──────────────────────────────────────────────
  { test: (cmd) => ['look', 'l', 'describe'].includes(cmd), exec: (cmd, args, rest) => { gameLook(); } },
  { test: (cmd) => ['examine', 'x', 'inspect', 'check'].includes(cmd), exec: (cmd, args, rest) => { gameExamine(args); } },
  { test: (cmd) => ['take', 'get', 'grab', 'pick', 'snag'].includes(cmd), exec: (cmd, args, rest) => { gameTake(args); } },
  { test: (cmd) => ['drop', 'put', 'place', 'set'].includes(cmd), exec: (cmd, args, rest) => { gameDrop(args); } },
  { test: (cmd) => ['leave'].includes(cmd), exec: (cmd, args, rest) => { gameGo(['outside']); } },
  { test: (cmd) => ['read'].includes(cmd), exec: (cmd, args, rest) => { gameRead(args); } },
  { test: (cmd) => ['open'].includes(cmd), exec: (cmd, args, rest) => { gameOpen(args); } },
  { test: (cmd) => ['close', 'shut'].includes(cmd), exec: (cmd, args, rest) => { gameClose(args); } },
  { test: (cmd) => ['message', 'messages', 'voicemail'].includes(cmd), exec: (cmd, args, rest) => { gamePlayMessage(); } },
  { test: (cmd) => ['insert', 'load'].includes(cmd), exec: (cmd, args, rest) => {
    const hasNonPlayingVHS  = ITEMS.some(i => i.shelvedVHS  && GameState.gInventory.includes(i.id) && i.id !== GameState.vhsPlayingId);
    const hasUnloadedTape   = ITEMS.some(i => i.shelvedTape && GameState.gInventory.includes(i.id) && GameState.cassettePlaying !== i.label);
    if      (GameState.gInventory.includes('floppy'))  gameInsertFloppy();
    else if (hasNonPlayingVHS)               gameInsertVHS();
    else if (hasUnloadedTape)                gameInsertCassette();
    else if (GameState.floppyInserted)                 addLine("The disk is already in the drive.");
    else                                     addLine("You're not holding anything to insert.");
  } },
  { test: (cmd) => ['eject', 'remove'].includes(cmd), exec: (cmd, args, rest) => {
    if      (GameState.floppyInserted)  gameEjectFloppy();
    else if (GameState.vhsPlayingId)    gameEjectVHS();
    else if (GameState.cassettePlaying) gameEjectCassette();
    else                      addLine("Nothing to eject.");
  } },
  { test: (cmd) => ['rewind'].includes(cmd), exec: (cmd, args, rest) => {
    const rwTarget = args.join(' ');
    const rwCassette = /cassette|tape|boombox/.test(rwTarget);
    const rwVCR      = !rwTarget || /vcr|vhs|video/.test(rwTarget);
    if (rwCassette || (GameState.cassettePlaying && !GameState.vhsPlayingId && !rwVCR)) {
      if (!GameState.cassettePlaying) { addLine("There's no tape in the boombox."); return; }
      if (!GameState.boomBoxOn)       { addLine("The boombox is off.");              return; }
      addLine('You press rewind. The boombox whirs. The tape spools back.');
    } else {
      if (!GameState.vhsPlayingId) { addLine("There's no tape in the VCR."); return; }
      if (!GameState.vcrOn)        { addLine("The VCR is off.");              return; }
      addLine('The VCR rewinds. The tape chirps back to the beginning.');
    }
  } },
  { test: (cmd) => ['play'].includes(cmd), exec: (cmd, args, rest) => { gamePlay(args); } },
  { test: (cmd) => ['stop'].includes(cmd), exec: (cmd, args, rest) => { gameStop(args); } },
  { test: (cmd) => ['sit'].includes(cmd), exec: (cmd, args, rest) => { gameSit(args); } },
  { test: (cmd) => ['stand', 'rise'].includes(cmd), exec: (cmd, args, rest) => { gameStand(); } },
  { test: (cmd) => ['go', 'walk', 'move', 'enter', 'head', 'travel'].includes(cmd), exec: (cmd, args, rest) => { gameGo(args); } },
  { test: (cmd) => ['north', 'n'].includes(cmd), exec: (cmd, args, rest) => { gameGo(['north']); } },
  { test: (cmd) => ['south', 's'].includes(cmd), exec: (cmd, args, rest) => { gameGo(['south']); } },
  { test: (cmd) => ['east', 'e'].includes(cmd), exec: (cmd, args, rest) => { gameGo(['east']); } },
  { test: (cmd) => ['west', 'w'].includes(cmd), exec: (cmd, args, rest) => { gameGo(['west']); } },
  { test: (cmd) => ['watch'].includes(cmd), exec: (cmd, args, rest) => { gameWatch(args); } },
  { test: (cmd) => ['listen', 'hear'].includes(cmd), exec: (cmd, args, rest) => { gameListen(args); } },
  { test: (cmd) => ['smell', 'sniff'].includes(cmd), exec: (cmd, args, rest) => { gameSmell(args); } },
  { test: (cmd) => ['touch', 'feel', 'rub', 'tap', 'pet'].includes(cmd), exec: (cmd, args, rest) => { gameTouch(args); } },
  { test: (cmd) => ['fill', 'pour'].includes(cmd), exec: (cmd, args, rest) => {
    if      (GameState.coffeePotState === 'empty')     gameFillCarafe();
    else if (GameState.gInventory.includes('glass'))   gameFillGlass();
    else                                     gameFillMug();
  } },
  { test: (cmd) => ['drink', 'sip'].includes(cmd), exec: (cmd, args, rest) => { gameDrink(args); } },
  { test: (cmd) => ['cook', 'fry'].includes(cmd), exec: (cmd, args, rest) => { gameCook(args); } },
  { test: (cmd) => ['eat', 'consume'].includes(cmd), exec: (cmd, args, rest) => { gameEat(args); } },
  { test: (cmd) => ['use'].includes(cmd), exec: (cmd, args, rest) => { gameUse(args); } },
  { test: (cmd) => ['inventory', 'i', 'inv', 'items', 'carrying'].includes(cmd), exec: (cmd, args, rest) => { gameInventory(); } },
  { test: (cmd) => ['wait', 'z'].includes(cmd), exec: (cmd, args, rest) => {
    addLine('Time passes.');
    if (GameState.coffeePotState === 'brewing') checkBrew();
  } },
  { test: (cmd) => ['turn'].includes(cmd), exec: (cmd, args, rest) => { addLine('Turn what on or off?'); } },
  { test: (cmd) => ['throw', 'toss', 'discard'].includes(cmd), exec: (cmd, args, rest) => { gameThrowAway(args); } },
  { test: (cmd) => ['push', 'shove'].includes(cmd), exec: (cmd, args, rest) => { addLine("That doesn't budge."); } },
  { test: (cmd) => ['pull'].includes(cmd), exec: (cmd, args, rest) => { addLine('You give it a tug. Nothing moves.'); } },
  { test: (cmd) => ['sleep', 'nap'].includes(cmd), exec: (cmd, args, rest) => { addLine("You're not tired enough for that."); } },
  { test: (cmd) => ['think'].includes(cmd), exec: (cmd, args, rest) => { addLine('Your mind wanders.'); } },
  { test: (cmd) => ['dance'].includes(cmd), exec: (cmd, args, rest) => { addLine('You shuffle in place for a moment.'); } },
  { test: (cmd) => ['yell', 'shout', 'scream'].includes(cmd), exec: (cmd, args, rest) => { addLine('Your voice echoes off the walls.'); } },
  { test: (cmd) => ['sing'].includes(cmd), exec: (cmd, args, rest) => {
    addLine(GameState.recordPlaying ? `You hum along with ${GameState.recordPlaying}.` : 'You hum to yourself.');
  } },
  { test: (cmd) => ['wave'].includes(cmd), exec: (cmd, args, rest) => { addLine('You wave at nobody in particular.'); } },
  { test: (cmd) => ['score'].includes(cmd), exec: (cmd, args, rest) => { addLine('There is no score. Just the room.'); } },
  { test: (cmd) => ['map'].includes(cmd), exec: (cmd, args, rest) => { gameMap(); } },
  { test: (cmd) => ['where'].includes(cmd), exec: (cmd, args, rest) => {
    const _w = GameState.playerArea;
    if      (!_w)                                       addLine('You\\'re standing in the middle of the living room.');
    else if (_w === 'desk' || _w === 'chair')           addLine('You\\'re at the desk.');
    else if (_w === 'sofa')                             addLine(GameState.seated ? 'You\\'re sitting on the sofa.' : 'You\\'re near the sofa.');
    else if (_w === 'kitchen')                          addLine('You\\'re in the kitchen.');
    else if (_w === 'shelf')                            addLine('You\\'re at the record shelf.');
    else if (_w === 'north')                            addLine('You\\'re at the north shelves.');
    else if (_w === 'ne')                               addLine('You\\'re in the northeast corner, near the boombox and cassettes.');
  } },
  { test: (cmd) => ['about', 'credits', 'info'].includes(cmd), exec: (cmd, args, rest) => { addLine('West Philly Simulator 93. A small apartment, October 1993. Made for one person. Everyone else is welcome to look around.'); } },
  { test: (cmd) => ['xyzzy', 'plugh'].includes(cmd), exec: (cmd, args, rest) => { addLine('Nothing happens.'); } },
  { test: (cmd) => ['fart'].includes(cmd), exec: (cmd, args, rest) => {
    addLine(GameState.seated ? 'You let one go into the sofa cushion. Cracker opens one eye.' : 'You rip one. The room is unimpressed.');
    addLine('It lingers.', 'dim');
    GameState.farted = true;
  } },
  { test: (cmd) => ['die', 'kill', 'murder'].includes(cmd), exec: (cmd, args, rest) => { addLine('This is not that kind of game. You are fine.'); } },
  { test: (cmd) => ['kill yourself', 'kys'].includes(cmd), exec: (cmd, args, rest) => { addLine('How about no. Make some scrapple instead.'); } },
  { test: (cmd) => ['sex', 'fuck', 'hump'].includes(cmd), exec: (cmd, args, rest) => { addLine("There's nobody here but you and a sleeping cat. Have some dignity."); } },
  { test: (cmd) => ['pee', 'piss', 'urinate'].includes(cmd), exec: (cmd, args, rest) => { addLine('The bathroom is not modeled. You hold it.'); } },
  { test: (cmd) => ['poop', 'shit', 'defecate'].includes(cmd), exec: (cmd, args, rest) => { addLine('Absolutely not.'); } },
  { test: (cmd) => ['eat cat', 'eat cracker'].includes(cmd), exec: (cmd, args, rest) => { addLine('Cracker shifts in her sleep, instinctively aware of your depravity.'); } },
  { test: (cmd) => ['pet cat', 'pet cracker'].includes(cmd), exec: (cmd, args, rest) => { addLine('You give her a scratch behind the ear. She doesn\\'t wake up but purrs louder.'); } },
  { test: (cmd) => ['sudo'].includes(cmd), exec: (cmd, args, rest) => { addLine('This is not that kind of computer.'); } },
  { test: (cmd) => ['hack'].includes(cmd), exec: (cmd, args, rest) => { addLine('You stare at the monitor. The monitor stares back.'); } },
  { test: (cmd) => ['flip table', 'flip'].includes(cmd), exec: (cmd, args, rest) => {
    if (GameState.scrappleInPan && GameState.stoveOn && !GameState.scrappleCooked) {
      GameState.scrappleCooked = true;
      addLine('The scrapple sizzles and crisps up. You flip the pieces with the knife.');
      addLine('Edges go golden-brown. The kitchen smells like Saturday morning.');
      addLine('');
      addLine('Breakfast is ready.', 'dim');
    } else if (GameState.scrappleInPan && !GameState.stoveOn) {
      addLine("The stove isn't on. Nothing to flip yet.");
    } else if (GameState.playerArea === 'kitchen') {
      addLine("There's nothing here that needs flipping.");
    } else {
      addLine('You grab the edge of the desk, reconsider, and let go.');
    }
  } },
  { test: (cmd) => ['panic'].includes(cmd), exec: (cmd, args, rest) => { addLine('You take a breath. The rain helps.'); } },
  { test: (cmd) => ['transcript', 'script', 'export'].includes(cmd), exec: (cmd, args, rest) => { gameTranscript(); } },
  { test: (cmd) => ['help', '?'].includes(cmd), exec: (cmd, args, rest) => { gameHelp(); } },
  { test: (cmd) => ['quit', 'exit', 'bye'].includes(cmd), exec: (cmd, args, rest) => {
    addLine('');
    addLine('You leave the living room.', 'dim');
    addLine('──────────────────────────────────────────────────────────────────', 'dim');
    addLine('');
    SystemState.state = 'shell';
    showPrompt();
    return 'QUIT';
  } }
];

function handleGameCommand(raw) {
  addLine('> ' + raw, 'hi');

  const trimmed = raw.trim();
  if (!trimmed) { addLine(''); promptEl.textContent = '> '; inputEl.value = ''; return; }

  if (GameState.gHistory[GameState.gHistory.length - 1] !== trimmed) GameState.gHistory.push(trimmed);
  GameState.gHistIdx = -1;

  // Consume pending verb
  const pv = GameState.pendingVerb;
  GameState.pendingVerb = null;

  // Probe verb before full tokenisation so pronoun resolution can weight by verb
  const rawVerb = trimmed.toLowerCase().split(/\\s+/)[0];

  // FocusStack-aware pronoun substitution: resolves 'it'/'that'/'this'/'one'
  // against the semantic focus rather than just the last regex match.
  const subbed = ContextManager.resolvePronouns(trimmed, rawVerb);

  const tokens = subbed.toLowerCase().split(/\\s+/);
  let cmd    = tokens[0];
  const args   = tokens.slice(1);
  const rest   = args.join(' ');
  
  // Normalize multi-word nonsense commands that check full string
  const fullCmd = tokens.join(' ');
  if (['eat cat', 'eat cracker', 'pet cat', 'pet cracker', 'kill yourself', 'kys', 'flip table'].includes(fullCmd)) {
      cmd = fullCmd;
  }

  // Record structured intent in ActionHistory for future disambiguation
  ContextManager.push({ verb: cmd, object: rest, area: GameState.playerArea });

  // ── Command dispatch ──────────────────────────────────────────
  const matched = VERB_REGISTRY.find(v => v.test(cmd, args, rest));

  if (matched) {
    if (matched.exec(cmd, args, rest) === 'QUIT') return;
  } else {
    if (pv) { handleGameCommand(pv + ' ' + trimmed); return; }
    // Context-aware fallback — mid-process hints instead of a dead end
    if      (GameState.coffeePotState === 'empty')                          addLine("The carafe's empty — still need to fill it with water.", 'dim');
    else if (GameState.coffeePotState === 'water')                          addLine("Water's in the reservoir. Still need a filter in the basket.", 'dim');
    else if (GameState.coffeePotState === 'filter')                         addLine("Filter's in. Still need the coffee grounds.", 'dim');
    else if (GameState.coffeePotState === 'grounds')                        addLine("Everything's in. Start the maker.", 'dim');
    else if (GameState.coffeePotState === 'brewing')                        addLine("Coffee's brewing. Check back in a minute.", 'dim');
    else if (GameState.scrappleCooked)                                      addLine("The scrapple's done in the pan. Eat it before it gets cold.", 'dim');
    else if (GameState.scrappleInPan && GameState.stoveOn && !GameState.scrappleCooked)         addLine("The scrapple's sizzling. It needs another minute or two.", 'dim');
    else if (GameState.scrappleInPan && !GameState.stoveOn)                           addLine("The scrapple's in the pan. The stove is still off.", 'dim');
    else if (GameState.floppyInserted && !GameState.floppyRead)                       addLine("There's a floppy disk in the drive. You can read what's on it.", 'dim');
    else                                                          addLine("That doesn't seem to do anything.", 'dim');
  }

  // Nudge to eject once after reading, on the next non-eject command
"""

with open('/Users/sev/Projects/FloppyLetters/FloppyLetter2601/engine.js', 'r') as f:
    text = f.read()

start_marker = "function handleGameCommand(raw) {"
end_marker = "  // Nudge to eject once after reading, on the next non-eject command"

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Markers not found.")
    exit(1)

new_text = text[:start_idx] + registry_code + text[end_idx:]

with open('/Users/sev/Projects/FloppyLetters/FloppyLetter2601/engine.js', 'w') as f:
    f.write(new_text)

print("Done replacement.")
