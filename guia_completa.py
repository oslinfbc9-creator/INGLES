# ============================================================
# GUÍA DE LOS 300 VERBOS MÁS IMPORTANTES DEL INGLÉS
# Crea carpeta, CSV y PDF automáticamente
# Requisito: pip install --user reportlab
# ============================================================

import os
import csv
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.units import cm

# ============================================================
# CONFIGURACIÓN
# ============================================================
CARPETA = "guia_verbos_ingles"
CSV_NOMBRE = "verbos.csv"
PDF_NOMBRE = "guia_300_verbos.pdf"

# ============================================================
# LOS 300 VERBOS
# Formato: (base, pasado, participio, -ing, significado, ejemplo)
# ============================================================
VERBOS = [
    # --- IRREGULARES (1-100) ---
    ("be", "was/were", "been", "being", "ser/estar", "I want to be a doctor. (Quiero ser médico.)"),
    ("have", "had", "had", "having", "tener", "I have two brothers. (Tengo dos hermanos.)"),
    ("do", "did", "done", "doing", "hacer", "What do you do? (¿A qué te dedicas?)"),
    ("say", "said", "said", "saying", "decir", "She said hello. (Ella dijo hola.)"),
    ("go", "went", "gone", "going", "ir", "I go to school. (Voy a la escuela.)"),
    ("get", "got", "gotten/got", "getting", "obtener/conseguir", "I got a new job. (Conseguí un nuevo trabajo.)"),
    ("make", "made", "made", "making", "hacer/fabricar", "I make dinner. (Preparo la cena.)"),
    ("know", "knew", "known", "knowing", "saber/conocer", "I know the answer. (Sé la respuesta.)"),
    ("think", "thought", "thought", "thinking", "pensar", "I think so. (Creo que sí.)"),
    ("take", "took", "taken", "taking", "tomar/llevar", "Take the book. (Toma el libro.)"),
    ("see", "saw", "seen", "seeing", "ver", "I can see you. (Puedo verte.)"),
    ("come", "came", "come", "coming", "venir", "Come here. (Ven aquí.)"),
    ("give", "gave", "given", "giving", "dar", "Give me the pen. (Dame el bolígrafo.)"),
    ("find", "found", "found", "finding", "encontrar", "I found my keys. (Encontré mis llaves.)"),
    ("tell", "told", "told", "telling", "decir/contar", "Tell me the truth. (Dime la verdad.)"),
    ("feel", "felt", "felt", "feeling", "sentir", "I feel happy. (Me siento feliz.)"),
    ("become", "became", "become", "becoming", "convertirse", "She became a teacher. (Ella se hizo maestra.)"),
    ("leave", "left", "left", "leaving", "dejar/salir", "I leave at 8. (Salgo a las 8.)"),
    ("put", "put", "put", "putting", "poner", "Put it on the table. (Ponlo en la mesa.)"),
    ("mean", "meant", "meant", "meaning", "significar", "What does it mean? (¿Qué significa?)"),
    ("keep", "kept", "kept", "keeping", "mantener/guardar", "Keep the change. (Quédate con el cambio.)"),
    ("let", "let", "let", "letting", "dejar/permitir", "Let me help you. (Déjame ayudarte.)"),
    ("begin", "began", "begun", "beginning", "comenzar", "Let's begin. (Empecemos.)"),
    ("hear", "heard", "heard", "hearing", "oír", "I can hear you. (Puedo oírte.)"),
    ("run", "ran", "run", "running", "correr", "I run every day. (Corro todos los días.)"),
    ("hold", "held", "held", "holding", "sostener", "Hold my hand. (Toma mi mano.)"),
    ("bring", "brought", "brought", "bringing", "traer", "Bring some water. (Trae agua.)"),
    ("write", "wrote", "written", "writing", "escribir", "Write your name. (Escribe tu nombre.)"),
    ("sit", "sat", "sat", "sitting", "sentarse", "Please sit down. (Por favor, siéntate.)"),
    ("stand", "stood", "stood", "standing", "estar de pie", "Stand up, please. (Por favor, ponte de pie.)"),
    ("lose", "lost", "lost", "losing", "perder", "Don't lose hope. (No pierdas la esperanza.)"),
    ("pay", "paid", "paid", "paying", "pagar", "I'll pay for dinner. (Yo pago la cena.)"),
    ("meet", "met", "met", "meeting", "conocer/encontrar", "Nice to meet you. (Encantado de conocerte.)"),
    ("set", "set", "set", "setting", "poner/establecer", "Set the table. (Pon la mesa.)"),
    ("lead", "led", "led", "leading", "liderar", "She leads the team. (Ella lidera el equipo.)"),
    ("understand", "understood", "understood", "understanding", "entender", "I understand you. (Te entiendo.)"),
    ("speak", "spoke", "spoken", "speaking", "hablar", "Do you speak English? (¿Hablas inglés?)"),
    ("read", "read", "read", "reading", "leer", "I read every night. (Leo cada noche.)"),
    ("spend", "spent", "spent", "spending", "gastar/pasar", "I spent $50. (Gasté 50 dólares.)"),
    ("grow", "grew", "grown", "growing", "crecer", "Plants grow fast. (Las plantas crecen rápido.)"),
    ("win", "won", "won", "winning", "ganar", "We won the game. (Ganamos el juego.)"),
    ("buy", "bought", "bought", "buying", "comprar", "I bought a new car. (Compré un coche nuevo.)"),
    ("send", "sent", "sent", "sending", "enviar", "Send me an email. (Envíame un correo.)"),
    ("build", "built", "built", "building", "construir", "They built a house. (Construyeron una casa.)"),
    ("fall", "fell", "fallen", "falling", "caer", "Don't fall! (¡No te caigas!)"),
    ("cut", "cut", "cut", "cutting", "cortar", "Cut the paper. (Corta el papel.)"),
    ("sell", "sold", "sold", "selling", "vender", "They sell fruit. (Venden fruta.)"),
    ("break", "broke", "broken", "breaking", "romper", "Don't break it! (¡No lo rompas!)"),
    ("drive", "drove", "driven", "driving", "conducir", "I drive to work. (Conduzco al trabajo.)"),
    ("hit", "hit", "hit", "hitting", "golpear", "He hit the ball. (Él golpeó la pelota.)"),
    ("eat", "ate", "eaten", "eating", "comer", "I eat breakfast. (Desayuno.)"),
    ("catch", "caught", "caught", "catching", "atrapar", "Catch the ball! (¡Atrapa la pelota!)"),
    ("draw", "drew", "drawn", "drawing", "dibujar", "I draw pictures. (Dibujo imágenes.)"),
    ("choose", "chose", "chosen", "choosing", "elegir", "Choose one. (Elige uno.)"),
    ("wear", "wore", "worn", "wearing", "llevar puesto", "She wears glasses. (Ella usa gafas.)"),
    ("shoot", "shot", "shot", "shooting", "disparar", "Don't shoot! (¡No dispares!)"),
    ("drink", "drank", "drunk", "drinking", "beber", "Drink water. (Bebe agua.)"),
    ("sing", "sang", "sung", "singing", "cantar", "She sings well. (Ella canta bien.)"),
    ("fly", "flew", "flown", "flying", "volar", "Birds fly. (Los pájaros vuelan.)"),
    ("swim", "swam", "swum", "swimming", "nadar", "I swim in summer. (Nado en verano.)"),
    ("teach", "taught", "taught", "teaching", "enseñar", "She teaches math. (Ella enseña matemáticas.)"),
    ("throw", "threw", "thrown", "throwing", "lanzar", "Throw the ball. (Lanza la pelota.)"),
    ("sleep", "slept", "slept", "sleeping", "dormir", "I sleep 8 hours. (Duermo 8 horas.)"),
    ("fight", "fought", "fought", "fighting", "luchar/pelear", "Don't fight! (¡No peleen!)"),
    ("wake", "woke", "woken", "waking", "despertar", "Wake up! (¡Despierta!)"),
    ("forget", "forgot", "forgotten", "forgetting", "olvidar", "Don't forget. (No olvides.)"),
    ("freeze", "froze", "frozen", "freezing", "congelar", "Water freezes. (El agua se congela.)"),
    ("hide", "hid", "hidden", "hiding", "esconder", "Hide the money. (Esconde el dinero.)"),
    ("ride", "rode", "ridden", "riding", "montar", "I ride a bike. (Monto en bici.)"),
    ("ring", "rang", "rung", "ringing", "sonar", "The phone rings. (El teléfono suena.)"),
    ("rise", "rose", "risen", "rising", "levantarse/subir", "The sun rises. (El sol sale.)"),
    ("shake", "shook", "shaken", "shaking", "agitar", "Shake the bottle. (Agita la botella.)"),
    ("shine", "shone", "shone", "shining", "brillar", "The stars shine. (Las estrellas brillan.)"),
    ("show", "showed", "shown", "showing", "mostrar", "Show me the way. (Muéstrame el camino.)"),
    ("sink", "sank", "sunk", "sinking", "hundir", "The boat sank. (El barco se hundió.)"),
    ("steal", "stole", "stolen", "stealing", "robar", "Don't steal! (¡No robes!)"),
    ("strike", "struck", "struck", "striking", "golpear", "He struck the table. (Él golpeó la mesa.)"),
    ("swear", "swore", "sworn", "swearing", "jurar", "I swear it's true. (Juro que es verdad.)"),
    ("sweep", "swept", "swept", "sweeping", "barrer", "Sweep the floor. (Barre el piso.)"),
    ("tear", "tore", "torn", "tearing", "rasgar", "Don't tear the paper. (No rasgues el papel.)"),
    ("bite", "bit", "bitten", "biting", "morder", "The dog bites. (El perro muerde.)"),
    ("blow", "blew", "blown", "blowing", "soplar", "Blow the candles. (Sopla las velas.)"),
    ("feed", "fed", "fed", "feeding", "alimentar", "Feed the cat. (Alimenta al gato.)"),
    ("flee", "fled", "fled", "fleeing", "huir", "They fled the city. (Huyeron de la ciudad.)"),
    ("forgive", "forgave", "forgiven", "forgiving", "perdonar", "Forgive me. (Perdóname.)"),
    ("hang", "hung", "hung", "hanging", "colgar", "Hang the picture. (Cuelga el cuadro.)"),
    ("lay", "laid", "laid", "laying", "colocar/acostar", "Lay the baby down. (Acuesta al bebé.)"),
    ("light", "lit", "lit", "lighting", "encender", "Light the candle. (Enciende la vela.)"),
    ("seek", "sought", "sought", "seeking", "buscar", "Seek help. (Busca ayuda.)"),
    ("slide", "slid", "slid", "sliding", "deslizar", "Slide the door. (Desliza la puerta.)"),
    ("stick", "stuck", "stuck", "sticking", "pegar", "Stick it here. (Pégalo aquí.)"),
    ("sting", "stung", "stung", "stinging", "picar", "Bees sting. (Las abejas pican.)"),
    ("swing", "swung", "swung", "swinging", "balancear", "Swing the bat. (Bate la pelota.)"),
    ("wet", "wet", "wet", "wetting", "mojar", "Don't wet the floor. (No mojes el piso.)"),
    ("beat", "beat", "beaten", "beating", "golpear/vencer", "Beat the eggs. (Bate los huevos.)"),
    ("bend", "bent", "bent", "bending", "doblar", "Bend your knees. (Dobla las rodillas.)"),
    ("bind", "bound", "bound", "binding", "atar", "Bind the books. (Ata los libros.)"),
    ("bleed", "bled", "bled", "bleeding", "sangrar", "My nose bleeds. (Me sangra la nariz.)"),
    ("breed", "bred", "bred", "breeding", "criar", "They breed dogs. (Crian perros.)"),
    ("cast", "cast", "cast", "casting", "lanzar/emitir", "Cast your vote. (Emite tu voto.)"),

    # --- REGULARES (101-300) ---
    ("want", "wanted", "wanted", "wanting", "querer", "I want water. (Quiero agua.)"),
    ("look", "looked", "looked", "looking", "mirar", "Look at me. (Mírame.)"),
    ("use", "used", "used", "using", "usar", "Use this pen. (Usa este bolígrafo.)"),
    ("work", "worked", "worked", "working", "trabajar", "I work here. (Trabajo aquí.)"),
    ("call", "called", "called", "calling", "llamar", "Call me later. (Llámame luego.)"),
    ("try", "tried", "tried", "trying", "intentar", "Try again. (Inténtalo otra vez.)"),
    ("ask", "asked", "asked", "asking", "preguntar/pedir", "Ask him. (Pregúntale.)"),
    ("need", "needed", "needed", "needing", "necesitar", "I need help. (Necesito ayuda.)"),
    ("seem", "seemed", "seemed", "seeming", "parecer", "You seem tired. (Pareces cansado.)"),
    ("help", "helped", "helped", "helping", "ayudar", "Help me. (Ayúdame.)"),
    ("talk", "talked", "talked", "talking", "hablar", "Let's talk. (Hablemos.)"),
    ("turn", "turned", "turned", "turning", "girar", "Turn left. (Gira a la izquierda.)"),
    ("start", "started", "started", "starting", "empezar", "Start now. (Empieza ahora.)"),
    ("play", "played", "played", "playing", "jugar/tocar", "I play guitar. (Toco la guitarra.)"),
    ("move", "moved", "moved", "moving", "mover(se)", "Move the chair. (Mueve la silla.)"),
    ("like", "liked", "liked", "liking", "gustar", "I like pizza. (Me gusta la pizza.)"),
    ("live", "lived", "lived", "living", "vivir", "I live in Madrid. (Vivo en Madrid.)"),
    ("believe", "believed", "believed", "believing", "creer", "I believe you. (Te creo.)"),
    ("happen", "happened", "happened", "happening", "ocurrir", "It happened fast. (Ocurrió rápido.)"),
    ("provide", "provided", "provided", "providing", "proporcionar", "They provide food. (Proporcionan comida.)"),
    ("include", "included", "included", "including", "incluir", "The price includes tax. (El precio incluye impuestos.)"),
    ("continue", "continued", "continued", "continuing", "continuar", "Continue reading. (Continúa leyendo.)"),
    ("learn", "learned", "learned", "learning", "aprender", "I learn English. (Aprendo inglés.)"),
    ("change", "changed", "changed", "changing", "cambiar", "Change your mind. (Cambia de opinión.)"),
    ("watch", "watched", "watched", "watching", "ver/observar", "Watch TV. (Mira TV.)"),
    ("follow", "followed", "followed", "following", "seguir", "Follow me. (Sígueme.)"),
    ("stop", "stopped", "stopped", "stopping", "parar", "Stop the car. (Para el coche.)"),
    ("create", "created", "created", "creating", "crear", "Create a file. (Crea un archivo.)"),
    ("open", "opened", "opened", "opening", "abrir", "Open the door. (Abre la puerta.)"),
    ("walk", "walked", "walked", "walking", "caminar", "I walk to school. (Camino a la escuela.)"),
    ("offer", "offered", "offered", "offering", "ofrecer", "They offered help. (Ofrecieron ayuda.)"),
    ("remember", "remembered", "remembered", "remembering", "recordar", "Remember my name. (Recuerda mi nombre.)"),
    ("love", "loved", "loved", "loving", "amar", "I love you. (Te amo.)"),
    ("consider", "considered", "considered", "considering", "considerar", "Consider the options. (Considera las opciones.)"),
    ("appear", "appeared", "appeared", "appearing", "aparecer", "He appeared suddenly. (Apareció de repente.)"),
    ("wait", "waited", "waited", "waiting", "esperar", "Wait for me. (Espérame.)"),
    ("serve", "served", "served", "serving", "servir", "Serve the food. (Sirve la comida.)"),
    ("die", "died", "died", "dying", "morir", "Plants die without water. (Las plantas mueren sin agua.)"),
    ("expect", "expected", "expected", "expecting", "esperar", "I expect success. (Espero éxito.)"),
    ("stay", "stayed", "stayed", "staying", "quedarse", "Stay here. (Quédate aquí.)"),
    ("reach", "reached", "reached", "reaching", "alcanzar", "Reach the top. (Alcanza la cima.)"),
    ("kill", "killed", "killed", "killing", "matar", "Don't kill insects. (No mates insectos.)"),
    ("remain", "remained", "remained", "remaining", "permanecer", "Remain calm. (Mantén la calma.)"),
    ("suggest", "suggested", "suggested", "suggesting", "sugerir", "I suggest this. (Sugiero esto.)"),
    ("raise", "raised", "raised", "raising", "levantar", "Raise your hand. (Levanta la mano.)"),
    ("pass", "passed", "passed", "passing", "pasar", "Pass the salt. (Pasa la sal.)"),
    ("require", "required", "required", "requiring", "requerir", "It requires time. (Requiere tiempo.)"),
    ("report", "reported", "reported", "reporting", "reportar", "Report the issue. (Reporta el problema.)"),
    ("decide", "decided", "decided", "deciding", "decidir", "Decide now. (Decide ahora.)"),
    ("pull", "pulled", "pulled", "pulling", "tirar de", "Pull the door. (Tira de la puerta.)"),
    ("enter", "entered", "entered", "entering", "entrar", "Enter the room. (Entra a la habitación.)"),
    ("return", "returned", "returned", "returning", "volver/devolver", "Return the book. (Devuelve el libro.)"),
    ("explain", "explained", "explained", "explaining", "explicar", "Explain this. (Explica esto.)"),
    ("hope", "hoped", "hoped", "hoping", "esperar", "I hope so. (Espero que sí.)"),
    ("develop", "developed", "developed", "developing", "desarrollar", "Develop an app. (Desarrolla una app.)"),
    ("carry", "carried", "carried", "carrying", "cargar/llevar", "Carry the bag. (Lleva la bolsa.)"),
    ("receive", "received", "received", "receiving", "recibir", "I received a gift. (Recibí un regalo.)"),
    ("agree", "agreed", "agreed", "agreeing", "estar de acuerdo", "I agree. (Estoy de acuerdo.)"),
    ("support", "supported", "supported", "supporting", "apoyar", "I support you. (Te apoyo.)"),
    ("produce", "produced", "produced", "producing", "producir", "They produce cars. (Producen coches.)"),
    ("cover", "covered", "covered", "covering", "cubrir", "Cover the food. (Cubre la comida.)"),
    ("cause", "caused", "caused", "causing", "causar", "It caused problems. (Causó problemas.)"),
    ("point", "pointed", "pointed", "pointing", "señalar", "Point the way. (Señala el camino.)"),
    ("listen", "listened", "listened", "listening", "escuchar", "Listen to me. (Escúchame.)"),
    ("realize", "realized", "realized", "realizing", "darse cuenta", "I realized my mistake. (Me di cuenta de mi error.)"),
    ("plan", "planned", "planned", "planning", "planear", "Plan the trip. (Planifica el viaje.)"),
    ("save", "saved", "saved", "saving", "salvar/ahorrar", "Save money. (Ahorra dinero.)"),
    ("add", "added", "added", "adding", "añadir", "Add some salt. (Añade un poco de sal.)"),
    ("allow", "allowed", "allowed", "allowing", "permitir", "Allow me. (Permíteme.)"),
    ("accept", "accepted", "accepted", "accepting", "aceptar", "Accept the offer. (Acepta la oferta.)"),
    ("achieve", "achieved", "achieved", "achieving", "lograr", "Achieve your goals. (Logra tus metas.)"),
    ("admit", "admitted", "admitted", "admitting", "admitir", "I admit my error. (Admito mi error.)"),
    ("affect", "affected", "affected", "affecting", "afectar", "It affects everyone. (Afecta a todos.)"),
    ("afford", "afforded", "afforded", "affording", "permitirse", "I can't afford it. (No puedo permitírmelo.)"),
    ("aim", "aimed", "aimed", "aiming", "apuntar", "Aim carefully. (Apunta con cuidado.)"),
    ("announce", "announced", "announced", "announcing", "anunciar", "They announced the news. (Anunciaron la noticia.)"),
    ("answer", "answered", "answered", "answering", "responder", "Answer the phone. (Contesta el teléfono.)"),
    ("apply", "applied", "applied", "applying", "aplicar/solicitar", "Apply for a job. (Solicita un trabajo.)"),
    ("argue", "argued", "argued", "arguing", "discutir", "Don't argue. (No discutas.)"),
    ("arrange", "arranged", "arranged", "arranging", "organizar", "Arrange the meeting. (Organiza la reunión.)"),
    ("arrive", "arrived", "arrived", "arriving", "llegar", "I arrived early. (Llegué temprano.)"),
    ("attack", "attacked", "attacked", "attacking", "atacar", "Don't attack. (No ataques.)"),
    ("avoid", "avoided", "avoided", "avoiding", "evitar", "Avoid the traffic. (Evita el tráfico.)"),
    ("base", "based", "based", "basing", "basar", "Base it on facts. (Básalo en hechos.)"),
    ("behave", "behaved", "behaved", "behaving", "comportarse", "Behave yourself. (Compórtate.)"),
    ("belong", "belonged", "belonged", "belonging", "pertenecer", "It belongs to me. (Me pertenece.)"),
    ("borrow", "borrowed", "borrowed", "borrowing", "pedir prestado", "Can I borrow it? (¿Puedo pedirlo prestado?)"),
    ("bother", "bothered", "bothered", "bothering", "molestar", "Don't bother me. (No me molestes.)"),
    ("brush", "brushed", "brushed", "brushing", "cepillar", "Brush your teeth. (Cepíllate los dientes.)"),
    ("burn", "burned", "burned", "burning", "quemar", "Don't burn the toast. (No quemes la tostada.)"),
    ("calculate", "calculated", "calculated", "calculating", "calcular", "Calculate the total. (Calcula el total.)"),
    ("care", "cared", "cared", "caring", "importar/cuidar", "I care about you. (Me importas.)"),
    ("celebrate", "celebrated", "celebrated", "celebrating", "celebrar", "Celebrate your birthday. (Celebra tu cumpleaños.)"),
    ("challenge", "challenged", "challenged", "challenging", "desafiar", "Challenge yourself. (Desafíate.)"),
    ("check", "checked", "checked", "checking", "comprobar", "Check the answer. (Comprueba la respuesta.)"),
    ("clean", "cleaned", "cleaned", "cleaning", "limpiar", "Clean the room. (Limpia la habitación.)"),
    ("climb", "climbed", "climbed", "climbing", "subir/escalar", "Climb the mountain. (Escala la montaña.)"),
    ("close", "closed", "closed", "closing", "cerrar", "Close the door. (Cierra la puerta.)"),
    ("collect", "collected", "collected", "collecting", "coleccionar", "Collect stamps. (Colecciona sellos.)"),
    ("compare", "compared", "compared", "comparing", "comparar", "Compare prices. (Compara precios.)"),
    ("complain", "complained", "complained", "complaining", "quejarse", "Don't complain. (No te quejes.)"),
    ("complete", "completed", "completed", "completing", "completar", "Complete the form. (Completa el formulario.)"),
    ("concentrate", "concentrated", "concentrated", "concentrating", "concentrarse", "Concentrate on work. (Concéntrate en el trabajo.)"),
    ("concern", "concerned", "concerned", "concerning", "preocupar", "It concerns me. (Me preocupa.)"),
    ("confirm", "confirmed", "confirmed", "confirming", "confirmar", "Confirm the booking. (Confirma la reserva.)"),
    ("connect", "connected", "connected", "connecting", "conectar", "Connect the cable. (Conecta el cable.)"),
    ("contain", "contained", "contained", "containing", "contener", "It contains sugar. (Contiene azúcar.)"),
    ("contribute", "contributed", "contributed", "contributing", "contribuir", "Contribute to society. (Contribuye a la sociedad.)"),
    ("control", "controlled", "controlled", "controlling", "controlar", "Control yourself. (Contrólate.)"),
    ("cook", "cooked", "cooked", "cooking", "cocinar", "Cook dinner. (Cocina la cena.)"),
    ("copy", "copied", "copied", "copying", "copiar", "Copy the text. (Copia el texto.)"),
    ("count", "counted", "counted", "counting", "contar", "Count the money. (Cuenta el dinero.)"),
    ("cross", "crossed", "crossed", "crossing", "cruzar", "Cross the street. (Cruza la calle.)"),
    ("cry", "cried", "cried", "crying", "llorar", "Don't cry. (No llores.)"),
    ("damage", "damaged", "damaged", "damaging", "dañar", "It damaged the car. (Dañó el coche.)"),
    ("dance", "danced", "danced", "dancing", "bailar", "Let's dance. (Bailemos.)"),
    ("deliver", "delivered", "delivered", "delivering", "entregar", "Deliver the package. (Entrega el paquete.)"),
    ("demand", "demanded", "demanded", "demanding", "exigir", "They demand justice. (Exigen justicia.)"),
    ("deny", "denied", "denied", "denying", "negar", "Don't deny it. (No lo niegues.)"),
    ("depend", "depended", "depended", "depending", "depender", "It depends on you. (Depende de ti.)"),
    ("describe", "described", "described", "describing", "describir", "Describe the scene. (Describe la escena.)"),
    ("deserve", "deserved", "deserved", "deserving", "merecer", "You deserve it. (Te lo mereces.)"),
    ("design", "designed", "designed", "designing", "diseñar", "Design a logo. (Diseña un logo.)"),
    ("destroy", "destroyed", "destroyed", "destroying", "destruir", "Don't destroy it. (No lo destruyas.)"),
    ("determine", "determined", "determined", "determining", "determinar", "Determine the cause. (Determina la causa.)"),
    ("discover", "discovered", "discovered", "discovering", "descubrir", "They discovered gold. (Descubrieron oro.)"),
    ("discuss", "discussed", "discussed", "discussing", "discutir", "Discuss the plan. (Discute el plan.)"),
    ("divide", "divided", "divided", "dividing", "dividir", "Divide the work. (Divide el trabajo.)"),
    ("doubt", "doubted", "doubted", "doubting", "dudar", "I doubt it. (Lo dudo.)"),
    ("drag", "dragged", "dragged", "dragging", "arrastrar", "Drag the file. (Arrastra el archivo.)"),
    ("drop", "dropped", "dropped", "dropping", "dejar caer", "Don't drop it. (No lo dejes caer.)"),
    ("earn", "earned", "earned", "earning", "ganar (dinero)", "Earn a living. (Gánate la vida.)"),
    ("educate", "educated", "educated", "educating", "educar", "Educate children. (Educa a los niños.)"),
    ("employ", "employed", "employed", "employing", "emplear", "They employ 50 people. (Emplean a 50 personas.)"),
    ("encourage", "encouraged", "encouraged", "encouraging", "animar", "Encourage him. (Anímalo.)"),
    ("enjoy", "enjoyed", "enjoyed", "enjoying", "disfrutar", "Enjoy the party. (Disfruta la fiesta.)"),
    ("ensure", "ensured", "ensured", "ensuring", "asegurar", "Ensure quality. (Asegura la calidad.)"),
    ("escape", "escaped", "escaped", "escaping", "escapar", "Escape from prison. (Escapa de la prisión.)"),
    ("establish", "established", "established", "establishing", "establecer", "Establish rules. (Establece reglas.)"),
    ("examine", "examined", "examined", "examining", "examinar", "Examine the evidence. (Examina la evidencia.)"),
    ("exist", "existed", "existed", "existing", "existir", "It doesn't exist. (No existe.)"),
    ("expand", "expanded", "expanded", "expanding", "expandir", "Expand the business. (Expande el negocio.)"),
    ("experience", "experienced", "experienced", "experiencing", "experimentar", "Experience new things. (Experimenta cosas nuevas.)"),
    ("express", "expressed", "expressed", "expressing", "expresar", "Express your feelings. (Expresa tus sentimientos.)"),
    ("extend", "extended", "extended", "extending", "extender", "Extend the deadline. (Extiende el plazo.)"),
    ("face", "faced", "faced", "facing", "enfrentar", "Face your fears. (Enfrenta tus miedos.)"),
    ("fail", "failed", "failed", "failing", "fallar", "Don't fail. (No falles.)"),
    ("fear", "feared", "feared", "fearing", "temer", "Don't fear failure. (No temas al fracaso.)"),
    ("fill", "filled", "filled", "filling", "llenar", "Fill the glass. (Llena el vaso.)"),
    ("finish", "finished", "finished", "finishing", "terminar", "Finish your work. (Termina tu trabajo.)"),
    ("fit", "fitted", "fitted", "fitting", "caber/ajustar", "It doesn't fit. (No queda bien.)"),
    ("fix", "fixed", "fixed", "fixing", "arreglar", "Fix the car. (Arregla el coche.)"),
    ("focus", "focused", "focused", "focusing", "enfocarse", "Focus on the task. (Enfócate en la tarea.)"),
    ("force", "forced", "forced", "forcing", "forzar", "Don't force it. (No lo fuerces.)"),
    ("form", "formed", "formed", "forming", "formar", "Form a line. (Forma una fila.)"),
    ("gain", "gained", "gained", "gaining", "ganar", "Gain experience. (Gana experiencia.)"),
    ("gather", "gathered", "gathered", "gathering", "reunir", "Gather the team. (Reúne al equipo.)"),
    ("greet", "greeted", "greeted", "greeting", "saludar", "Greet the guests. (Saluda a los invitados.)"),
    ("guess", "guessed", "guessed", "guessing", "adivinar", "Guess the answer. (Adivina la respuesta.)"),
    ("handle", "handled", "handled", "handling", "manejar", "Handle the situation. (Maneja la situación.)"),
    ("hate", "hated", "hated", "hating", "odiar", "I hate traffic. (Odio el tráfico.)"),
    ("heat", "heated", "heated", "heating", "calentar", "Heat the water. (Calienta el agua.)"),
    ("hire", "hired", "hired", "hiring", "contratar", "They hired me. (Me contrataron.)"),
    ("identify", "identified", "identified", "identifying", "identificar", "Identify the problem. (Identifica el problema.)"),
    ("ignore", "ignored", "ignored", "ignoring", "ignorar", "Don't ignore me. (No me ignores.)"),
    ("imagine", "imagined", "imagined", "imagining", "imaginar", "Imagine the future. (Imagina el futuro.)"),
    ("improve", "improved", "improved", "improving", "mejorar", "Improve your skills. (Mejora tus habilidades.)"),
    ("increase", "increased", "increased", "increasing", "aumentar", "Increase production. (Aumenta la producción.)"),
    ("inform", "informed", "informed", "informing", "informar", "Inform the boss. (Informa al jefe.)"),
    ("insist", "insisted", "insisted", "insisting", "insistir", "I insist. (Insisto.)"),
    ("intend", "intended", "intended", "intending", "pretender", "I intend to go. (Pretendo ir.)"),
    ("introduce", "introduced", "introduced", "introducing", "presentar", "Introduce yourself. (Preséntate.)"),
    ("invest", "invested", "invested", "investing", "invertir", "Invest in stocks. (Invierte en acciones.)"),
    ("involve", "involved", "involved", "involving", "involucrar", "Don't involve me. (No me involucres.)"),
    ("join", "joined", "joined", "joining", "unirse", "Join the club. (Únete al club.)"),
    ("judge", "judged", "judged", "judging", "juzgar", "Don't judge. (No juzgues.)"),
    ("jump", "jumped", "jumped", "jumping", "saltar", "Jump high. (Salta alto.)"),
    ("kick", "kicked", "kicked", "kicking", "patear", "Kick the ball. (Patea la pelota.)"),
    ("knock", "knocked", "knocked", "knocking", "llamar (puerta)", "Knock on the door. (Llama a la puerta.)"),
    ("laugh", "laughed", "laughed", "laughing", "reír", "Laugh out loud. (Ríe a carcajadas.)"),
    ("launch", "launched", "launched", "launching", "lanzar", "Launch the product. (Lanza el producto.)"),
    ("limit", "limited", "limited", "limiting", "limitar", "Limit the time. (Limita el tiempo.)"),
    ("link", "linked", "linked", "linking", "vincular", "Link the pages. (Vincula las páginas.)"),
    ("list", "listed", "listed", "listing", "listar", "List the items. (Lista los artículos.)"),
    ("load", "loaded", "loaded", "loading", "cargar", "Load the truck. (Carga el camión.)"),
    ("lock", "locked", "locked", "locking", "cerrar con llave", "Lock the door. (Cierra la puerta con llave.)"),
    ("maintain", "maintained", "maintained", "maintaining", "mantener", "Maintain order. (Mantén el orden.)"),
    ("manage", "managed", "managed", "managing", "gestionar/lograr", "Manage the project. (Gestiona el proyecto.)"),
    ("mark", "marked", "marked", "marking", "marcar", "Mark the date. (Marca la fecha.)"),
    ("marry", "married", "married", "marrying", "casarse", "They married young. (Se casaron jóvenes.)"),
    ("match", "matched", "matched", "matching", "coincidir", "The colors match. (Los colores coinciden.)"),
    ("matter", "mattered", "mattered", "mattering", "importar", "It doesn't matter. (No importa.)"),
    ("measure", "measured", "measured", "measuring", "medir", "Measure the room. (Mide la habitación.)"),
    ("mention", "mentioned", "mentioned", "mentioning", "mencionar", "Don't mention it. (No lo menciones.)"),
    ("mind", "minded", "minded", "minding", "importar", "Do you mind? (¿Te importa?)"),
    ("miss", "missed", "missed", "missing", "extrañar/perder", "I miss you. (Te extraño.)"),
    ("mix", "mixed", "mixed", "mixing", "mezclar", "Mix the ingredients. (Mezcla los ingredientes.)"),
    ("name", "named", "named", "naming", "nombrar", "Name the file. (Nombra el archivo.)"),
    ("notice", "noticed", "noticed", "noticing", "notar", "I noticed it. (Lo noté.)"),
    ("obtain", "obtained", "obtained", "obtaining", "obtener", "Obtain permission. (Obtén permiso.)"),
]

# ============================================================
# VERBOS DE POSICIÓN Y DIRECCIÓN
# ============================================================
POSICION_DIRECCION = [
    # --- POSICIÓN ---
    ("stand", "stood", "stood", "standing", "estar de pie", "She stood by the window. (Estaba de pie junto a la ventana.)"),
    ("sit", "sat", "sat", "sitting", "estar sentado", "He sat on the chair. (Estaba sentado en la silla.)"),
    ("lie", "lay", "lain", "lying", "estar tumbado", "The cat lies on the bed. (El gato está tumbado en la cama.)"),
    ("put", "put", "put", "putting", "poner", "Put the book on the table. (Pon el libro en la mesa.)"),
    ("place", "placed", "placed", "placing", "colocar", "She placed the vase there. (Ella colocó el jarrón allí.)"),
    ("rest", "rested", "rested", "resting", "reposar", "His hand rested on her shoulder. (Su mano reposaba en su hombro.)"),
    ("hang", "hung", "hung", "hanging", "colgar", "The picture hangs on the wall. (El cuadro cuelga de la pared.)"),
    ("lay", "laid", "laid", "laying", "colocar horizontalmente", "Lay the baby on the bed. (Acuesta al bebé en la cama.)"),
    ("lean", "leaned", "leaned", "leaning", "apoyarse", "He leaned against the wall. (Se apoyó contra la pared.)"),
    ("kneel", "knelt", "knelt", "kneeling", "arrodillarse", "She knelt by the bed. (Se arrodilló junto a la cama.)"),
    ("crouch", "crouched", "crouched", "crouching", "agacharse", "He crouched behind the car. (Se agachó detrás del coche.)"),
    ("locate", "located", "located", "locating", "ubicar", "The hotel is located downtown. (El hotel está ubicado en el centro.)"),
    ("situate", "situated", "situated", "situating", "situar", "The house is situated on a hill. (La casa está situada en una colina.)"),
    ("position", "positioned", "positioned", "positioning", "posicionar", "He positioned himself near the door. (Se posicionó cerca de la puerta.)"),

    # --- DIRECCIÓN / MOVIMIENTO ---
    ("go", "went", "gone", "going", "ir", "Go into the room. (Entra en la habitación.)"),
    ("come", "came", "come", "coming", "venir", "Come here. (Ven aquí.)"),
    ("walk", "walked", "walked", "walking", "caminar", "Walk towards me. (Camina hacia mí.)"),
    ("run", "ran", "run", "running", "correr", "Run around the park. (Corre alrededor del parque.)"),
    ("move", "moved", "moved", "moving", "moverse", "Move forward. (Avanza.)"),
    ("enter", "entered", "entered", "entering", "entrar", "Enter the building. (Entra al edificio.)"),
    ("exit", "exited", "exited", "exiting", "salir", "Exit through the back. (Sal por detrás.)"),
    ("leave", "left", "left", "leaving", "salir/marcharse", "Leave the room. (Sal de la habitación.)"),
    ("arrive", "arrived", "arrived", "arriving", "llegar", "Arrive at 5 pm. (Llega a las 5.)"),
    ("return", "returned", "returned", "returning", "volver", "Return home. (Vuelve a casa.)"),
    ("climb", "climbed", "climbed", "climbing", "subir", "Climb the stairs. (Sube las escaleras.)"),
    ("descend", "descended", "descended", "descending", "descender", "Descend the hill. (Desciende la colina.)"),
    ("cross", "crossed", "crossed", "crossing", "cruzar", "Cross the bridge. (Cruza el puente.)"),
    ("pass", "passed", "passed", "passing", "pasar", "Pass through the tunnel. (Pasa por el túnel.)"),
    ("turn", "turned", "turned", "turning", "girar", "Turn right. (Gira a la derecha.)"),
    ("approach", "approached", "approached", "approaching", "acercarse", "Approach the stage. (Acércate al escenario.)"),
    ("follow", "followed", "followed", "following", "seguir", "Follow the path. (Sigue el sendero.)"),
    ("escape", "escaped", "escaped", "escaping", "escapar", "Escape through the window. (Escapa por la ventana.)"),
    ("travel", "traveled", "traveled", "traveling", "viajar", "Travel to Paris. (Viaja a París.)"),
    ("drive", "drove", "driven", "driving", "conducir", "Drive to the airport. (Conduce al aeropuerto.)"),
]

# ============================================================
# FUNCIONES
# ============================================================
def crear_carpeta():
    """Crea la carpeta de trabajo si no existe y entra en ella."""
    os.makedirs(CARPETA, exist_ok=True)
    os.chdir(CARPETA)
    print(f"📁 Carpeta creada: {os.getcwd()}")

def guardar_csv():
    """Guarda los verbos en un CSV (editable con Excel)."""
    with open(CSV_NOMBRE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["base", "pasado", "participio", "ing", "significado", "ejemplo"])
        writer.writerows(VERBOS)
    print(f"💾 CSV guardado: {CSV_NOMBRE} ({len(VERBOS)} verbos)")

def crear_tabla(datos, estilos):
    """Construye una tabla formateada con los verbos."""
    if not datos:
        return []

    estilo_celda = ParagraphStyle('celda', parent=estilos['Normal'], fontSize=8, leading=10)
    estilo_cab = ParagraphStyle('cab', parent=estilos['Normal'], fontSize=9, leading=11,
                                textColor=colors.white, alignment=1)

    cabecera = [Paragraph(c, estilo_cab) for c in
                ["Base", "Pasado", "Participio", "-ing", "Significado", "Ejemplo"]]
    filas = [cabecera]

    for v in datos:
        filas.append([Paragraph(str(campo), estilo_celda) for campo in v])

    tabla = Table(filas,
                  colWidths=[2.8*cm, 2.8*cm, 2.8*cm, 2.8*cm, 4*cm, 9.5*cm],
                  repeatRows=1)

    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F4E79')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F2F2F2')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return [tabla, Spacer(1, 0.5*cm)]

def generar_pdf():
    """Genera el PDF con las dos secciones."""
    doc = SimpleDocTemplate(
        PDF_NOMBRE, pagesize=landscape(A4),
        rightMargin=1.2*cm, leftMargin=1.2*cm,
        topMargin=1.2*cm, bottomMargin=1.2*cm
    )
    estilos = getSampleStyleSheet()
    historia = []

    # Portada
    historia.append(Paragraph("Guía de los 300 verbos más importantes del inglés", estilos['Title']))
    historia.append(Spacer(1, 0.5*cm))
    historia.append(Paragraph(
        "Conjugaciones (base, pasado, participio, -ing) + ejemplos de uso.<br/>"
        "Incluye una sección aparte de verbos de posición y dirección.",
        estilos['Normal']))
    historia.append(Spacer(1, 0.3*cm))
    historia.append(Paragraph(
        "<b>Fuentes de referencia:</b> Cambridge University Press (<i>English Grammar in Use</i>), "
        "Oxford University Press (<i>Oxford Learner's Grammar</i>), "
        "Randolph Quirk (<i>A University Grammar of English</i>).",
        ParagraphStyle('ref', parent=estilos['Normal'], fontSize=8, textColor=colors.grey)))
    historia.append(PageBreak())

    # Sección 1
    historia.append(Paragraph("1. Los 300 verbos más importantes", estilos['Heading1']))
    historia.append(Spacer(1, 0.3*cm))
    historia.extend(crear_tabla(VERBOS, estilos))

    # Sección 2
    historia.append(PageBreak())
    historia.append(Paragraph("2. Verbos de posición y dirección", estilos['Heading1']))
    historia.append(Spacer(1, 0.3*cm))
    historia.append(Paragraph(
        "Verbos que indican <b>posición</b> (estado, ubicación estática) o "
        "<b>dirección/movimiento</b> (desplazamiento).",
        estilos['Normal']))
    historia.append(Spacer(1, 0.3*cm))
    historia.extend(crear_tabla(POSICION_DIRECCION, estilos))

    doc.build(historia)
    print(f"📄 PDF generado: {PDF_NOMBRE}")

# ============================================================
# EJECUCIÓN
# ============================================================
if __name__ == "__main__":
    print("🚀 Iniciando generación de la guía...\n")
    crear_carpeta()
    guardar_csv()
    generar_pdf()
    print("\n✅ ¡Todo listo! Abre la carpeta y revisa el PDF.")