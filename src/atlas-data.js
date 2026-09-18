/* ---------------------------------------------------------------
   3D Body Atlas — region data
   Sequence follows a standard nursing head-to-toe assessment:
   general survey -> integument -> head -> face -> HEENT -> lymph ->
   cranial nerves -> neck -> posterior chest -> anterior chest ->
   heart -> breasts/axillae -> abdomen -> back/CVA -> extremities ->
   neuro -> GU.

   Coordinates are in model units on a ~1.8-unit figure, feet at y=0.
   `layer: true` categories are detail overlays, hidden until asked for.
--------------------------------------------------------------- */

const CATS = {
  general: { label: 'General',  color: 0x94a3b8 },
  skin:    { label: 'Skin',     color: 0xf472b6 },
  heent:   { label: 'HEENT',    color: 0x2dd4bf },
  lymph:   { label: 'Lymph',    color: 0xc084fc, layer: true },
  cn:      { label: 'Cranial N', color: 0xa78bfa, layer: true },
  resp:    { label: 'Resp',     color: 0x60a5fa },
  cardio:  { label: 'Cardio',   color: 0xf87171 },
  gi:      { label: 'GI',       color: 0xfb923c },
  gu:      { label: 'GU',       color: 0xfbbf24 },
  msk:     { label: 'MSK',      color: 0x4ade80 },
  vasc:    { label: 'Vascular', color: 0x22d3ee },
  neuro:   { label: 'Neuro',    color: 0x818cf8 },
};

const REGIONS = [

/* ---------- 1. General survey ---------- */
{
  id: 'general', label: 'General Survey & Vitals', cat: 'general',
  pos: [[0, 1.90, 0]],
  technique: 'Begin the moment you enter the room, before touching the patient. Observe level of consciousness and orientation (A&O x4), apparent distress, posture and gait, hygiene and grooming, body habitus, speech, affect, and odor. Then obtain vital signs: temperature, pulse, respirations, blood pressure, SpO2, and pain.',
  normal: 'Alert and oriented x4, no acute distress, appears stated age, steady gait, appropriate dress and hygiene, speech clear and appropriate.',
  watch: 'Altered or declining LOC, tripod positioning or accessory muscle use, cachexia, slurred speech, unsteady gait, fruity breath (DKA), unkempt appearance suggesting self-care deficit.',
  pearl: 'A&O x4 = person, place, time, and situation. The general survey is where most abnormal findings are first suspected — you are assessing before you ever lay hands on the patient.',
  quiz: [
    { q: 'A patient is oriented to person, place, and time but cannot say why they came to the hospital. How is this documented?', options: ['A&O x4', 'A&O x3', 'A&O x2', 'Unresponsive'], answer: 1, why: 'Oriented to person, place, and time = x3. The missing fourth sphere is situation.' },
    { q: 'Which of these belongs to the general survey rather than a focused system exam?', options: ['Auscultating breath sounds in all lobes', 'Palpating the abdomen in four quadrants', 'Observing posture, hygiene, and apparent distress', 'Testing deep tendon reflexes'], answer: 2, why: 'The general survey is observational and happens before hands-on system assessment.' },
  ],
},

/* ---------- 2. Integument ---------- */
{
  id: 'skin', label: 'Skin, Hair & Nails', cat: 'skin',
  pos: [[0.175, 1.30, 0.105]],
  technique: 'Inspect and palpate throughout the exam rather than as one isolated step. Assess color, temperature (back of your hand), moisture, texture, turgor (pinch over the clavicle or sternum, not the hand), edema, and any lesions or wounds. Inspect hair distribution and scalp, and nails for shape, color, and capillary refill.',
  normal: 'Warm, dry, intact, and appropriate to ethnicity. Turgor brisk with immediate recoil. Capillary refill under 3 seconds. Nail angle 160 degrees. No lesions, edema, or breakdown.',
  watch: 'Pallor, cyanosis, jaundice, or erythema. Tenting (dehydration). Diaphoresis. Non-blanchable erythema over bony prominences (stage 1 pressure injury). Clubbing (chronic hypoxia). Spoon nails (iron deficiency). Any new or changing lesion (ABCDE).',
  pearl: 'ABCDE for melanoma: Asymmetry, Border irregularity, Color variation, Diameter over 6 mm, Evolving. Check turgor over the clavicle in older adults — hand skin loses elasticity with age and gives false positives.',
  quiz: [
    { q: 'Where should skin turgor be assessed in an older adult?', options: ['Back of the hand', 'Over the clavicle or sternum', 'The forearm', 'The calf'], answer: 1, why: 'Hand skin loses elasticity with normal aging and falsely suggests dehydration. Clavicle or sternum is more reliable.' },
    { q: 'Non-blanchable erythema over the sacrum in an immobile patient indicates:', options: ['Stage 1 pressure injury', 'Stage 2 pressure injury', 'Normal reactive hyperemia', 'Cellulitis'], answer: 0, why: 'Intact skin with non-blanchable redness is a stage 1 pressure injury. If it blanches, it is reactive hyperemia.' },
  ],
},

/* ---------- 3. Head ---------- */
{
  id: 'head', label: 'Head & Scalp', cat: 'heent',
  pos: [[0, 1.75, -0.02]],
  technique: 'Inspect the skull for size, shape, and symmetry. Palpate the scalp and skull systematically for tenderness, masses, depressions, or step-offs. Inspect hair for texture, distribution, and lesions or infestation. Note facial symmetry at rest and with movement. Palpate the temporomandibular joint as the patient opens and closes.',
  normal: 'Normocephalic and atraumatic. Skull smooth and symmetric without tenderness, masses, or depressions. Hair evenly distributed. TMJ moves smoothly without click or pain.',
  watch: 'Palpable step-off or depression (skull fracture). Battle sign (mastoid bruising) or raccoon eyes (periorbital bruising) suggesting basilar skull fracture. Localized tenderness. TMJ crepitus or limited opening.',
  pearl: 'Normocephalic/atraumatic is abbreviated NCAT. Battle sign and raccoon eyes take hours to develop — their absence early does not rule out a basilar skull fracture.',
  quiz: [
    { q: 'Bruising over the mastoid process following head trauma is called:', options: ['Raccoon eyes', 'Battle sign', 'Cullen sign', 'Grey Turner sign'], answer: 1, why: 'Battle sign is retroauricular ecchymosis and suggests basilar skull fracture. Raccoon eyes are periorbital.' },
  ],
},

/* ---------- 4. Face ---------- */
{
  id: 'face', label: 'Face', cat: 'heent',
  pos: [[0, 1.60, 0.135]],
  technique: 'Inspect facial features for symmetry at rest, noting the palpebral fissures and nasolabial folds. Ask the patient to raise eyebrows, close eyes tightly, smile, show teeth, and puff cheeks (CN VII). Test light touch over the forehead, cheek, and jaw bilaterally, and have the patient clench the jaw (CN V). Palpate the frontal and maxillary sinuses for tenderness.',
  normal: 'Face symmetric at rest and with movement. Sensation intact to light touch in all three trigeminal branches. Jaw strength equal. No sinus tenderness.',
  watch: 'Facial droop. In stroke, forehead movement is spared because of bilateral cortical innervation; in Bell palsy the entire side including the forehead is affected. Unilateral numbness. Sinus tenderness with purulent drainage.',
  pearl: 'The forehead is the discriminator: droop that spares the forehead is central (stroke); droop that includes the forehead is peripheral (Bell palsy).',
  quiz: [
    { q: 'A patient has left facial droop but can still wrinkle the forehead on that side. This suggests:', options: ['Bell palsy', 'A central lesion such as stroke', 'Trigeminal neuralgia', 'A normal finding'], answer: 1, why: 'Forehead sparing indicates a central (upper motor neuron) lesion, because the forehead receives bilateral cortical innervation.' },
    { q: 'Which cranial nerve is tested by asking a patient to clench the jaw?', options: ['CN V', 'CN VII', 'CN IX', 'CN XI'], answer: 0, why: 'The trigeminal nerve (V) supplies the muscles of mastication and facial sensation.' },
  ],
},

/* ---------- 5. Eyes ---------- */
{
  id: 'eyes', label: 'Eyes', cat: 'heent',
  pos: [[-0.045, 1.638, 0.118], [0.045, 1.638, 0.118]],
  technique: 'Test visual acuity (Snellen) and visual fields by confrontation. Inspect lids, conjunctiva, and sclera. Assess pupils for size, shape, equality, and direct and consensual reaction to light, then accommodation (PERRLA). Test the six cardinal fields of gaze for extraocular movement. Assess the corneal light reflex.',
  normal: 'Visual acuity 20/20 with correction. Sclera white, conjunctiva pink and moist. Pupils equal, round, 2-4 mm, briskly reactive to light and accommodation. EOMs intact in all six fields without nystagmus.',
  watch: 'Anisocoria (unequal pupils). Fixed or sluggish pupils. A blown unilateral pupil is an emergency suggesting increased intracranial pressure. Scleral icterus (jaundice). Nystagmus. Sudden vision loss or new visual field cut.',
  pearl: 'PERRLA = Pupils Equal, Round, Reactive to Light and Accommodation. EOMs are CN III, IV, and VI together — the LR6-SO4 rule: Lateral Rectus is CN VI, Superior Oblique is CN IV, all the rest are CN III.',
  quiz: [
    { q: 'A previously alert patient now has a unilaterally dilated, non-reactive pupil. The priority interpretation is:', options: ['Normal variant anisocoria', 'Possible increased intracranial pressure — escalate immediately', 'Recent eye drops', 'Expected post-operative finding'], answer: 1, why: 'A new blown pupil suggests uncal herniation and rising ICP. This is an emergency requiring immediate escalation.' },
    { q: 'Which muscles does CN III NOT control?', options: ['Medial rectus', 'Lateral rectus and superior oblique', 'Inferior rectus', 'Superior rectus'], answer: 1, why: 'LR6-SO4: the lateral rectus is CN VI and the superior oblique is CN IV. CN III does the rest.' },
  ],
},

/* ---------- 6. Ears ---------- */
{
  id: 'ears', label: 'Ears & Hearing', cat: 'heent',
  pos: [[-0.132, 1.615, -0.005], [0.132, 1.615, -0.005]],
  technique: 'Inspect the auricle and external canal for discharge, lesions, or deformity. Palpate the tragus and mastoid for tenderness. Use an otoscope to view the canal and tympanic membrane, pulling the pinna up and back in adults (down and back in children under 3). Screen hearing with a whispered word test, and use Weber and Rinne with a tuning fork if loss is suspected.',
  normal: 'Auricles symmetric without lesions. Canal clear with minimal cerumen. Tympanic membrane pearly gray, translucent, with a visible cone of light and no bulging or perforation. Hearing intact to whispered voice bilaterally. Weber does not lateralize; Rinne AC > BC.',
  watch: 'Purulent discharge. Clear or bloody otorrhea after head trauma, which may be CSF. Red, bulging TM with loss of landmarks (otitis media). Sudden hearing loss. Weber lateralizing or Rinne BC > AC.',
  pearl: 'Adults: pull the pinna UP and BACK. Children under 3: DOWN and BACK. Weber lateralizes TO the bad ear in conductive loss and AWAY from the bad ear in sensorineural loss.',
  quiz: [
    { q: 'When examining the ear of an adult with an otoscope, the pinna is pulled:', options: ['Down and back', 'Up and back', 'Straight out', 'Up and forward'], answer: 1, why: 'Adults: up and back straightens the canal. Children under 3: down and back.' },
    { q: 'In the Weber test, sound lateralizes to the right ear. This is consistent with:', options: ['Conductive loss in the right ear or sensorineural loss in the left', 'Sensorineural loss in the right ear', 'Normal hearing', 'Bilateral conductive loss'], answer: 0, why: 'Weber lateralizes toward a conductive loss and away from a sensorineural loss.' },
  ],
},

/* ---------- 7. Nose ---------- */
{
  id: 'nose', label: 'Nose & Sinuses', cat: 'heent',
  pos: [[0, 1.593, 0.150]],
  technique: 'Inspect the external nose for symmetry and deformity. Check patency by occluding one naris at a time. Use a penlight or nasal speculum to inspect the mucosa, septum, and turbinates. Palpate and, if indicated, transilluminate the frontal and maxillary sinuses.',
  normal: 'Nose midline and symmetric. Both nares patent. Mucosa pink and moist. Septum midline without perforation. No discharge, polyps, or sinus tenderness.',
  watch: 'Epistaxis. Persistent clear rhinorrhea after head trauma (possible CSF leak — test for halo sign or glucose). Pale boggy turbinates (allergy). Purulent discharge with sinus tenderness and fever. Septal perforation.',
  pearl: 'Nasal flaring is an early sign of respiratory distress, particularly in infants and children — note it here and carry it to your respiratory assessment.',
  quiz: [
    { q: 'Clear fluid draining from the nose after a head injury should raise suspicion for:', options: ['Allergic rhinitis', 'CSF leak from a basilar skull fracture', 'Viral upper respiratory infection', 'Nasal polyps'], answer: 1, why: 'Clear rhinorrhea after head trauma may be CSF. Check for a halo sign and notify the provider immediately.' },
  ],
},

/* ---------- 8. Mouth ---------- */
{
  id: 'mouth', label: 'Mouth & Throat', cat: 'heent',
  pos: [[0, 1.546, 0.132]],
  technique: 'Inspect lips, buccal mucosa, gums, teeth, tongue, hard and soft palate, and the posterior pharynx with a light and tongue blade. Ask the patient to say "ah" and watch the soft palate and uvula rise symmetrically (CN IX and X). Test gag reflex if indicated. Ask the patient to stick out the tongue and move it side to side (CN XII). Note breath odor and swallowing.',
  normal: 'Lips and mucosa pink, moist, and intact. Teeth in good repair. Tongue midline with symmetric movement. Uvula rises midline with "ah". Tonsils 1+ or absent without exudate. Gag intact. Swallow without difficulty.',
  watch: 'Dry mucous membranes (dehydration). Uvula deviation (CN X lesion — it deviates AWAY from the affected side). Tongue deviation (CN XII — deviates TOWARD the affected side). Tonsillar exudate or asymmetry. Drooling or difficulty swallowing (airway risk). Absent gag (aspiration risk — hold oral intake).',
  pearl: 'An absent gag reflex means high aspiration risk: keep the patient NPO and escalate before any oral intake or medication.',
  quiz: [
    { q: 'A patient sticks out the tongue and it deviates to the left. The lesion is:', options: ['Right CN XII', 'Left CN XII', 'Right CN VII', 'Left CN X'], answer: 1, why: 'The tongue deviates TOWARD the side of a CN XII lesion.' },
    { q: 'Before giving oral medications to a post-stroke patient, the nurse should first:', options: ['Check the gag and swallow', 'Check blood pressure', 'Auscultate bowel sounds', 'Assess pupils'], answer: 0, why: 'An impaired gag or swallow creates aspiration risk. Swallow screening precedes any oral intake.' },
  ],
},

/* ---------- 9. Lymph nodes ---------- */
{
  id: 'lymph', label: 'Head & Neck Lymph Nodes', cat: 'lymph',
  pos: [[0, 1.47, 0.10]],
  technique: 'Palpate with the pads of your index and middle fingers using gentle circular motion, both sides at once, with the patient\'s neck slightly flexed toward the side being examined to relax the muscles. Move through the chain in a consistent order so nothing is missed. Note size, shape, consistency, mobility, tenderness, and whether nodes are discrete or matted.',
  normal: 'Nodes non-palpable, or small (under 1 cm), soft, round, mobile, discrete, and non-tender.',
  watch: 'Hard, fixed, matted, non-tender nodes over 1 cm suggest malignancy. Tender, warm, enlarged nodes suggest infection. Any palpable supraclavicular node is abnormal and warrants workup.',
  pearl: 'A palpable LEFT supraclavicular node is Virchow node — classically associated with abdominal or thoracic malignancy. Tender usually means infection; hard and fixed usually means cancer.',
  sub: [
    { name: '1. Preauricular', pos: [[-0.090, 1.618, 0.042], [0.090, 1.618, 0.042]], note: 'In front of the ear. Drains the eye, temporal scalp, and external ear.' },
    { name: '2. Postauricular (mastoid)', pos: [[-0.090, 1.618, -0.052], [0.090, 1.618, -0.052]], note: 'Over the mastoid process behind the ear. Classically enlarged in rubella.' },
    { name: '3. Occipital', pos: [[-0.052, 1.578, -0.128], [0.052, 1.578, -0.128]], note: 'At the base of the skull posteriorly. Drains the posterior scalp.' },
    { name: '4. Tonsillar (jugulodigastric)', pos: [[-0.074, 1.545, 0.040], [0.074, 1.545, 0.040]], note: 'At the angle of the mandible. Enlarged in pharyngitis and tonsillitis.' },
    { name: '5. Submandibular', pos: [[-0.052, 1.520, 0.074], [0.052, 1.520, 0.074]], note: 'Midway along the underside of the jaw. Drains the tongue, lips, and mouth.' },
    { name: '6. Submental', pos: [[0, 1.512, 0.094]], note: 'Midline beneath the chin. Drains the lower lip, floor of mouth, and tongue tip.' },
    { name: '7. Superficial cervical', pos: [[-0.064, 1.462, 0.050], [0.064, 1.462, 0.050]], note: 'Overlying the sternocleidomastoid muscle.' },
    { name: '8. Posterior cervical', pos: [[-0.070, 1.452, -0.050], [0.070, 1.452, -0.050]], note: 'Along the anterior edge of the trapezius. Enlarged in mononucleosis.' },
    { name: '9. Deep cervical chain', pos: [[-0.052, 1.438, 0.040], [0.052, 1.438, 0.040]], note: 'Deep to the sternocleidomastoid — hook your fingers around the muscle to palpate.' },
    { name: '10. Supraclavicular', pos: [[-0.100, 1.398, 0.050], [0.100, 1.398, 0.050]], note: 'In the angle above the clavicle. ALWAYS abnormal if palpable. Left side = Virchow node.' },
  ],
  quiz: [
    { q: 'A palpable, hard, fixed node above the left clavicle is known as:', options: ['Virchow node', 'Tonsillar node', 'Occipital node', 'Submental node'], answer: 0, why: 'The left supraclavicular (Virchow) node is classically associated with abdominal or thoracic malignancy.' },
    { q: 'Which lymph node characteristics most suggest malignancy rather than infection?', options: ['Tender, warm, and mobile', 'Hard, fixed, matted, and non-tender', 'Soft, under 1 cm, and mobile', 'Bilateral and tender'], answer: 1, why: 'Malignant nodes tend to be hard, fixed, matted, and painless. Infectious nodes are usually tender and mobile.' },
    { q: 'Posterior cervical lymphadenopathy in a teenager with sore throat and fatigue suggests:', options: ['Strep pharyngitis', 'Infectious mononucleosis', 'Dental abscess', 'Otitis externa'], answer: 1, why: 'Posterior cervical chain involvement is characteristic of mononucleosis.' },
  ],
},

/* ---------- 10. Cranial nerves ---------- */
{
  id: 'cranial', label: 'Cranial Nerves I–XII', cat: 'cn',
  pos: [[0, 1.70, 0.12]],
  technique: 'Screen systematically I through XII. Much of this is already done during the HEENT exam: pupils and EOMs (III, IV, VI), facial sensation and jaw strength (V), facial expression (VII), hearing (VIII), palate and uvula rise (IX, X), shoulder shrug and head turn (XI), and tongue protrusion (XII). Smell (I) is tested only when indicated.',
  normal: 'Cranial nerves II–XII grossly intact. CN I not routinely tested.',
  watch: 'Any new focal cranial nerve deficit is a red flag for stroke, mass, or raised intracranial pressure. Sudden onset with other neuro findings requires immediate escalation and stroke workup.',
  pearl: 'Names: On Old Olympus Towering Tops A Finn And German Viewed Some Hops. Function: Some Say Marry Money But My Brother Says Big Brains Matter Most (S = sensory, M = motor, B = both).',
  sub: [
    { name: 'I — Olfactory (S)', pos: [[0, 1.614, 0.136]], note: 'Smell. Occlude one naris and test a familiar odor. Not routinely screened.' },
    { name: 'II — Optic (S)', pos: [[0.060, 1.650, 0.108]], note: 'Vision. Snellen acuity and visual fields by confrontation.' },
    { name: 'III — Oculomotor (M)', pos: [[0.040, 1.662, 0.112]], note: 'Pupil constriction, lid elevation, and most eye movement. A blown pupil is a CN III emergency.' },
    { name: 'IV — Trochlear (M)', pos: [[0.024, 1.650, 0.118]], note: 'Superior oblique — moves the eye down and in. Tested with the cardinal fields.' },
    { name: 'V — Trigeminal (B)', pos: [[0.086, 1.585, 0.082]], note: 'Facial sensation in three branches plus muscles of mastication. Clench the jaw; test light touch.' },
    { name: 'VI — Abducens (M)', pos: [[0.066, 1.632, 0.100]], note: 'Lateral rectus — lateral gaze. Palsy causes inward deviation and horizontal diplopia.' },
    { name: 'VII — Facial (B)', pos: [[0.096, 1.556, 0.058]], note: 'Facial expression plus taste on the anterior two-thirds of the tongue. Smile, raise brows, puff cheeks.' },
    { name: 'VIII — Vestibulocochlear (S)', pos: [[0.128, 1.606, -0.010]], note: 'Hearing and balance. Whisper test, Weber and Rinne.' },
    { name: 'IX — Glossopharyngeal (B)', pos: [[0.022, 1.532, 0.104]], note: 'Gag reflex, swallowing, taste on the posterior third of the tongue. Tested with CN X.' },
    { name: 'X — Vagus (B)', pos: [[0.032, 1.478, 0.076]], note: 'Palate and uvula rise, gag, voice quality. Hoarseness or uvula deviation signals a lesion.' },
    { name: 'XI — Spinal accessory (M)', pos: [[0.074, 1.432, 0.014]], note: 'Sternocleidomastoid and trapezius. Shrug shoulders and turn head against resistance.' },
    { name: 'XII — Hypoglossal (M)', pos: [[0, 1.528, 0.112]], note: 'Tongue movement. Protrude the tongue — it deviates TOWARD a lesion.' },
  ],
  quiz: [
    { q: 'Which cranial nerves are assessed together when testing the six cardinal fields of gaze?', options: ['II, III, IV', 'III, IV, VI', 'IV, VI, VII', 'II, V, VII'], answer: 1, why: 'Extraocular movement is controlled by CN III, IV, and VI.' },
    { q: 'Asking a patient to shrug the shoulders against resistance tests:', options: ['CN X', 'CN XI', 'CN XII', 'CN VII'], answer: 1, why: 'The spinal accessory nerve (XI) innervates the trapezius and sternocleidomastoid.' },
    { q: 'Which cranial nerve is responsible for the gag reflex along with CN X?', options: ['CN VIII', 'CN IX', 'CN XI', 'CN V'], answer: 1, why: 'CN IX (glossopharyngeal) carries the afferent limb; CN X carries the efferent limb.' },
  ],
},

/* ---------- 11. Neck structures ---------- */
{
  id: 'neck-ant', label: 'Neck: Trachea, Thyroid, Carotids', cat: 'cardio',
  pos: [[0, 1.45, 0.085]],
  technique: 'Inspect the neck for symmetry and jugular venous distention with the head of the bed at 30-45 degrees. Palpate the trachea for midline position in the suprasternal notch. Palpate the thyroid from behind as the patient swallows. Auscultate each carotid with the bell for bruits BEFORE palpating, and never palpate both carotids at once.',
  normal: 'Trachea midline. Thyroid non-enlarged and non-tender, moves with swallowing. No JVD at 45 degrees. Carotid pulses 2+ and equal without bruits.',
  watch: 'Tracheal deviation (tension pneumothorax — deviates AWAY from the affected side). JVD (right heart failure, fluid overload, tamponade). Carotid bruit (stenosis). Enlarged or nodular thyroid.',
  pearl: 'Auscultate carotids before palpating, and one at a time — bilateral pressure can trigger a vagal response and drop heart rate and cerebral perfusion.',
  quiz: [
    { q: 'In a tension pneumothorax, the trachea deviates:', options: ['Toward the affected side', 'Away from the affected side', 'It remains midline', 'Downward'], answer: 1, why: 'Accumulating pressure pushes mediastinal structures away from the affected lung.' },
    { q: 'Why should the nurse avoid palpating both carotid arteries simultaneously?', options: ['It is uncomfortable', 'It can stimulate a vagal response and reduce cerebral perfusion', 'It gives a falsely high reading', 'It can dislodge a thyroid nodule'], answer: 1, why: 'Bilateral carotid pressure can trigger bradycardia and compromise cerebral blood flow.' },
  ],
},
{
  id: 'neck-post', label: 'Cervical Spine & Neck ROM', cat: 'msk',
  pos: [[0, 1.45, -0.085]],
  technique: 'Inspect alignment. Palpate the cervical spinous processes and paraspinal muscles for tenderness or step-off. If no trauma is suspected, assess active range of motion: flexion, extension, lateral bending, and rotation. Test neck flexion for nuchal rigidity.',
  normal: 'Cervical spine midline without tenderness or step-off. Full painless range of motion. Neck supple; chin reaches chest without resistance.',
  watch: 'Midline cervical tenderness after trauma — immobilize and do not test range of motion. Nuchal rigidity with fever and headache (meningitis). Limited or painful ROM.',
  pearl: 'Never assess neck range of motion in a patient with suspected cervical injury. Midline bony tenderness after trauma means the collar stays on.',
  quiz: [
    { q: 'A trauma patient reports midline cervical tenderness. The nurse should:', options: ['Assess full range of motion', 'Maintain spinal immobilization and notify the provider', 'Apply heat and reassess in an hour', 'Assist the patient to sit up'], answer: 1, why: 'Midline bony tenderness suggests possible cervical spine injury — immobilization is maintained and ROM is not tested.' },
  ],
},

/* ---------- 12-13. Lungs ---------- */
{
  id: 'chest-post', label: 'Posterior Thorax & Lungs', cat: 'resp',
  pos: [[0, 1.27, -0.16]],
  technique: 'Assessed FIRST in a standard head-to-toe, with the patient sitting and leaning slightly forward. Inspect the thorax shape and spinal alignment. Palpate for tenderness, chest expansion (thumbs at T9-T10), and tactile fremitus with the patient saying "ninety-nine". Percuss systematically side to side. Auscultate in a ladder pattern, comparing side to side, through a full breath cycle at each point.',
  normal: 'Thorax symmetric with a 1:2 anteroposterior to transverse ratio. Symmetric expansion. Fremitus equal bilaterally. Resonant to percussion. Vesicular breath sounds clear to the bases without adventitious sounds.',
  watch: 'Crackles (fluid — heart failure, pneumonia). Wheezes (narrowing — asthma, COPD). Diminished or absent sounds (pneumothorax, effusion, consolidation). Dullness to percussion (fluid or consolidation). Hyperresonance (air trapping). Barrel chest (COPD).',
  pearl: 'Compare side to side, never top to bottom on one side — asymmetry is the finding. Always listen through a full inspiration AND expiration at each spot.',
  quiz: [
    { q: 'Auscultation in the posterior chest should follow which pattern?', options: ['Down one entire side, then the other', 'Side to side in a ladder pattern, comparing symmetric points', 'Only over the lower lobes', 'Randomly, wherever sounds are heard'], answer: 1, why: 'Comparing symmetric points side to side is what reveals asymmetry, which is the clinically meaningful finding.' },
    { q: 'Dullness to percussion over the right lower lung field most likely indicates:', options: ['Pneumothorax', 'Pleural effusion or consolidation', 'Emphysema', 'Normal lung'], answer: 1, why: 'Dullness means fluid or solid tissue replacing air. Pneumothorax and emphysema cause hyperresonance.' },
  ],
},
{
  id: 'chest-ant', label: 'Anterior Thorax & Lungs', cat: 'resp',
  pos: [[0, 1.30, 0.155]],
  technique: 'Inspect rate, rhythm, depth, effort, and use of accessory muscles; note symmetry and any retractions. Palpate for tenderness, crepitus, and expansion. Percuss and auscultate the anterior and lateral fields in a ladder pattern, including the midaxillary line for the right middle lobe.',
  normal: 'Respirations 12-20, unlabored, regular, symmetric. No accessory muscle use or retractions. Clear vesicular breath sounds bilaterally; bronchial sounds over the trachea.',
  watch: 'Tachypnea or bradypnea. Accessory muscle use, retractions, nasal flaring, tripod positioning. Paradoxical chest movement (flail chest). Unilateral absent sounds with tracheal deviation and hypotension (tension pneumothorax — emergency). Stridor (upper airway obstruction).',
  pearl: 'The right middle lobe is only heard anteriorly and laterally — if you auscultate only the back, you miss it entirely.',
  quiz: [
    { q: 'Which lung lobe cannot be assessed from the posterior chest?', options: ['Right upper lobe', 'Right middle lobe', 'Left lower lobe', 'Right lower lobe'], answer: 1, why: 'The right middle lobe is auscultated anteriorly and at the right midaxillary line only.' },
    { q: 'Sudden onset of unilateral absent breath sounds, tracheal deviation, and hypotension indicates:', options: ['Pneumonia', 'Tension pneumothorax', 'Asthma exacerbation', 'Pulmonary edema'], answer: 1, why: 'This triad is a tension pneumothorax — a life threat requiring immediate decompression.' },
  ],
},

/* ---------- 14. Heart ---------- */
{
  id: 'heart', label: 'Heart / Precordium', cat: 'cardio',
  pos: [[-0.07, 1.20, 0.165]],
  technique: 'Inspect and palpate the precordium for heaves or thrills and locate the point of maximal impulse at the 5th intercostal space, midclavicular line. Auscultate the five valve areas with both diaphragm and bell: Aortic (2nd right ICS), Pulmonic (2nd left ICS), Erb point (3rd left ICS), Tricuspid (4th left ICS), Mitral/apex (5th left ICS MCL). Count the apical pulse for a full minute.',
  normal: 'PMI at the 5th ICS midclavicular line, about the size of a quarter. S1 and S2 crisp, regular rate and rhythm, 60-100. No murmurs, rubs, or gallops.',
  watch: 'Irregular rhythm. Murmur (turbulent flow). S3 gallop (volume overload, heart failure). S4 (stiff ventricle). Muffled heart sounds with JVD and hypotension (Beck triad — cardiac tamponade). Displaced PMI (cardiomegaly). Apical-radial pulse deficit (atrial fibrillation).',
  pearl: 'APE To Man = Aortic, Pulmonic, Erb, Tricuspid, Mitral. S1 (lub) is closure of the AV valves and marks the start of systole; S2 (dub) is closure of the semilunar valves.',
  quiz: [
    { q: 'Where is the point of maximal impulse normally palpated?', options: ['2nd ICS right sternal border', '5th ICS left midclavicular line', '4th ICS left sternal border', '2nd ICS left sternal border'], answer: 1, why: 'The PMI or apical impulse is at the 5th intercostal space, left midclavicular line.' },
    { q: 'Muffled heart sounds, jugular venous distention, and hypotension together are known as:', options: ['Beck triad — cardiac tamponade', 'Cushing triad — raised ICP', 'Virchow triad — thrombosis', 'Charcot triad — cholangitis'], answer: 0, why: 'Beck triad indicates cardiac tamponade, a life-threatening emergency.' },
    { q: 'An S3 heart sound in an older adult most commonly suggests:', options: ['Normal aging', 'Volume overload such as heart failure', 'Aortic stenosis', 'Dehydration'], answer: 1, why: 'S3 is a ventricular gallop from rapid filling into a volume-overloaded ventricle. It can be normal in children and young adults.' },
  ],
},

/* ---------- 15. Breasts & axillae ---------- */
{
  id: 'axillae', label: 'Breasts & Axillae', cat: 'lymph',
  pos: [[-0.16, 1.30, 0.045], [0.16, 1.30, 0.045]],
  technique: 'Inspect with arms at sides, raised overhead, and pressed on hips, looking for symmetry, dimpling, retraction, or skin change. Palpate all breast tissue systematically (vertical strip, wedge, or concentric circles) including the tail of Spence. Palpate the axillary nodes — central, anterior/pectoral, posterior/subscapular, and lateral — with the patient\'s arm supported and relaxed.',
  normal: 'Breasts symmetric without dimpling, retraction, or discharge. No masses. Axillary nodes non-palpable and non-tender.',
  watch: 'A fixed, hard, irregular, non-tender mass. Skin dimpling or peau d\'orange. Nipple retraction or spontaneous unilateral bloody discharge. Palpable, fixed axillary nodes.',
  pearl: 'The upper outer quadrant and the tail of Spence contain the most glandular tissue and are the most common site of breast cancer — do not skip into the axilla.',
  quiz: [
    { q: 'Most breast tumors are found in which location?', options: ['Lower inner quadrant', 'Upper outer quadrant and tail of Spence', 'Directly beneath the nipple', 'Lower outer quadrant'], answer: 1, why: 'The upper outer quadrant holds the most glandular tissue and is the most common tumor site.' },
  ],
},

/* ---------- 16. Abdomen ---------- */
{
  id: 'abdomen', label: 'Abdomen', cat: 'gi',
  pos: [[0, 1.03, 0.155]],
  technique: 'The ONE region where the order changes: Inspect, Auscultate, Percuss, then Palpate. Palpating first stimulates the bowel and falsifies your bowel sounds. Inspect contour, symmetry, and skin. Auscultate all four quadrants with the diaphragm — listen up to 5 minutes before calling bowel sounds absent. Percuss for tympany and organ borders. Palpate lightly then deeply in all four quadrants, saving any painful area for LAST.',
  normal: 'Abdomen flat to rounded, soft, non-tender, non-distended. Active bowel sounds (5-30 per minute) in all four quadrants. Tympanic to percussion. No masses, guarding, or organomegaly.',
  watch: 'Rigidity, involuntary guarding, or rebound tenderness (peritonitis). Absent bowel sounds after 5 minutes (ileus). High-pitched tinkling (obstruction). A pulsatile midline mass — DO NOT palpate deeply; suspect abdominal aortic aneurysm. Cullen sign (periumbilical bruising) or Grey Turner sign (flank bruising) suggest retroperitoneal bleeding.',
  pearl: 'Inspect, Auscultate, Percuss, Palpate — abdomen only. If you feel a pulsatile mass, stop palpating immediately and escalate.',
  quiz: [
    { q: 'What is the correct order of abdominal assessment?', options: ['Inspect, palpate, percuss, auscultate', 'Inspect, auscultate, percuss, palpate', 'Auscultate, inspect, palpate, percuss', 'Palpate, inspect, auscultate, percuss'], answer: 1, why: 'Auscultation precedes percussion and palpation because manipulating the abdomen alters bowel sounds.' },
    { q: 'While palpating, the nurse feels a pulsatile mass near the midline. The priority action is:', options: ['Palpate deeper to define the borders', 'Stop palpating and notify the provider immediately', 'Ask the patient to bear down', 'Percuss over the mass'], answer: 1, why: 'A pulsatile mass may be an abdominal aortic aneurysm. Continued palpation risks rupture.' },
    { q: 'How long must the nurse listen before documenting absent bowel sounds?', options: ['30 seconds', '1 minute', '5 minutes per quadrant', '10 seconds'], answer: 2, why: 'Bowel sounds are only called absent after listening a full 5 minutes in the quadrant.' },
  ],
},

/* ---------- 17. Back & CVA ---------- */
{
  id: 'back', label: 'Back, Spine & CVA Tenderness', cat: 'gu',
  pos: [[0, 1.05, -0.16]],
  technique: 'Inspect the spine for alignment and symmetry of the shoulders, scapulae, and iliac crests; look for scoliosis, kyphosis, or lordosis. Palpate the spinous processes and paraspinal muscles. Assess costovertebral angle tenderness by placing one palm over the CVA and striking it with the ulnar surface of your fist — this is for kidney assessment.',
  normal: 'Spine midline with normal curvature. No tenderness over spinous processes or paraspinal muscles. No CVA tenderness bilaterally.',
  watch: 'CVA tenderness (pyelonephritis or renal calculi). Lateral curvature (scoliosis). Midline tenderness after trauma. Grey Turner sign (flank ecchymosis).',
  pearl: 'CVA tenderness is a KIDNEY assessment, not a back assessment — it belongs with your renal findings even though you perform it on the back.',
  quiz: [
    { q: 'Positive costovertebral angle tenderness most suggests:', options: ['Lumbar muscle strain', 'Kidney inflammation such as pyelonephritis', 'Herniated disc', 'Spinal stenosis'], answer: 1, why: 'The CVA overlies the kidneys; percussion tenderness suggests renal inflammation or infection.' },
  ],
},

/* ---------- 18-20. Upper extremities ---------- */
{
  id: 'arms', label: 'Upper Arms & Shoulders', cat: 'msk',
  pos: [[-0.21, 1.24, 0.03], [0.21, 1.24, 0.03]],
  technique: 'Inspect for symmetry, muscle bulk, and skin. Palpate joints for warmth, swelling, and tenderness. Assess active and passive range of motion at the shoulder and elbow. Test muscle strength against resistance and grade 0-5. Palpate the brachial pulse medial to the biceps tendon.',
  normal: 'Arms symmetric with equal muscle bulk. Full painless ROM. Strength 5/5 and equal bilaterally. Brachial pulses 2+ and equal.',
  watch: 'Unilateral weakness or drift (stroke). Asymmetric muscle bulk or atrophy. Joint swelling, warmth, or deformity. Diminished or absent pulse. Never take blood pressure in an arm with a dialysis fistula, on the side of a mastectomy with node dissection, or with a PICC.',
  pearl: 'Strength grading: 5 = full against resistance, 4 = against some resistance, 3 = against gravity only, 2 = with gravity removed, 1 = flicker, 0 = none. Pronator drift is a sensitive early stroke sign.',
  quiz: [
    { q: 'Muscle strength that overcomes gravity but not added resistance is graded:', options: ['5/5', '4/5', '3/5', '2/5'], answer: 2, why: '3/5 is full range against gravity only. 4/5 overcomes some resistance.' },
    { q: 'Blood pressure should NOT be taken in an arm that has:', options: ['An AV dialysis fistula', 'A healed fracture from childhood', 'A tattoo', 'Mild eczema'], answer: 0, why: 'Cuff pressure can damage or clot an AV fistula. Also avoid the mastectomy side and limbs with a PICC.' },
  ],
},
{
  id: 'hands', label: 'Hands, Nails & Radial Pulse', cat: 'msk',
  pos: [[-0.245, 0.72, 0.06], [0.245, 0.72, 0.06]],
  technique: 'Inspect hands and nails for color, clubbing, deformity, and tremor. Test grip strength bilaterally and simultaneously. Palpate radial pulses bilaterally and compare. Assess capillary refill at the nail bed. Assess fine motor coordination and sensation.',
  normal: 'Hands warm and pink. Grips strong and equal. Radial pulses 2+ and equal. Capillary refill under 3 seconds. Nail angle 160 degrees. No tremor or deformity.',
  watch: 'Unequal grips (focal neurologic deficit). Clubbing (chronic hypoxia). Delayed capillary refill (poor perfusion). Cyanosis. Tremor. Ulnar deviation and swan-neck deformity (rheumatoid arthritis). Heberden nodes (osteoarthritis).',
  pearl: 'Test grips simultaneously — asymmetry is the finding, and you will miss it testing one at a time. Pulse grading: 0 absent, 1+ weak/thready, 2+ normal, 3+ increased, 4+ bounding.',
  quiz: [
    { q: 'A pulse documented as 2+ is:', options: ['Absent', 'Weak and thready', 'Normal', 'Bounding'], answer: 2, why: 'Scale: 0 absent, 1+ weak/thready, 2+ normal, 3+ increased, 4+ bounding.' },
    { q: 'Clubbing of the fingernails most commonly indicates:', options: ['Acute infection', 'Chronic hypoxia', 'Dehydration', 'Recent trauma'], answer: 1, why: 'Clubbing (nail angle over 180 degrees) reflects chronic hypoxemia from cardiopulmonary disease.' },
  ],
},

/* ---------- 21-23. Lower extremities ---------- */
{
  id: 'hips', label: 'Hips & Pelvis', cat: 'msk',
  pos: [[-0.145, 0.82, 0.04], [0.145, 0.82, 0.04]],
  technique: 'Inspect leg length and alignment and observe gait if the patient can ambulate. Palpate the iliac crests for level symmetry. Assess hip range of motion — flexion, extension, abduction, adduction, internal and external rotation — and note pain or limitation. Palpate the femoral pulse below the inguinal ligament.',
  normal: 'Legs equal length and aligned. Iliac crests level. Full painless hip ROM. Femoral pulses 2+ and equal. Steady gait.',
  watch: 'A shortened, externally rotated leg after a fall — classic hip fracture. Pain with weight bearing or passive ROM. Unequal leg length. Absent femoral pulse.',
  pearl: 'Shortened and externally rotated after a fall means hip fracture until proven otherwise — do not range the hip, keep the patient non-weight-bearing, and get imaging.',
  quiz: [
    { q: 'An older adult falls and the right leg appears shortened and externally rotated. This suggests:', options: ['Hip fracture', 'Hip dislocation posteriorly', 'Muscle strain', 'Sciatica'], answer: 0, why: 'Shortening with external rotation is the classic presentation of a femoral neck (hip) fracture.' },
  ],
},
{
  id: 'knees', label: 'Thighs & Knees', cat: 'msk',
  pos: [[-0.105, 0.60, 0.065], [0.105, 0.60, 0.065]],
  technique: 'Inspect for symmetry, swelling, and muscle bulk. Palpate the knee for warmth, effusion, and tenderness; check the patellar ballottement if swelling is present. Assess active and passive range of motion and stability. Test quadriceps strength. Elicit the patellar deep tendon reflex.',
  normal: 'Thighs symmetric with equal bulk. Knees without swelling, warmth, or effusion. Full ROM and stable ligaments. Patellar reflex 2+ bilaterally.',
  watch: 'Effusion or warmth (infection, injury, gout). Instability or locking. Unilateral thigh swelling with tenderness (DVT). Asymmetric or absent reflexes. Quadriceps atrophy.',
  pearl: 'Deep tendon reflexes grade 0-4+ with 2+ normal. Hyperreflexia (3-4+) suggests an upper motor neuron problem; hyporeflexia suggests a lower motor neuron or peripheral problem.',
  quiz: [
    { q: 'A deep tendon reflex graded 4+ with clonus suggests:', options: ['Normal finding', 'Upper motor neuron lesion', 'Lower motor neuron lesion', 'Peripheral neuropathy'], answer: 1, why: 'Hyperreflexia with clonus points to an upper motor neuron lesion. Diminished reflexes suggest lower motor neuron or peripheral problems.' },
  ],
},
{
  id: 'legs', label: 'Lower Legs: Edema & DVT', cat: 'vasc',
  pos: [[-0.105, 0.28, 0.045], [0.105, 0.28, 0.045]],
  technique: 'Inspect for color, hair distribution, varicosities, and skin changes. Palpate for temperature and for pitting edema over the tibia and medial malleolus, pressing 5 seconds and grading 1+ to 4+. Compare calf circumference bilaterally at the same landmark. Palpate the posterior tibial pulse behind the medial malleolus.',
  normal: 'Legs symmetric, warm, with even color and hair distribution. No edema. Calf circumference equal. Posterior tibial pulses 2+ and equal. Non-tender calves.',
  watch: 'UNILATERAL calf swelling, warmth, redness, and tenderness — suspect DVT, do NOT massage the calf, and escalate. Bilateral pitting edema (heart, renal, or hepatic failure). Cool, pale, hairless, shiny skin with absent pulses (arterial insufficiency). Brown discoloration with irregular ulcers around the medial malleolus (venous insufficiency).',
  pearl: 'UNILATERAL = vascular/DVT. BILATERAL = systemic (cardiac, renal, hepatic). Arterial ulcers are painful, punched-out, and on the toes and lateral malleolus; venous ulcers are wet, irregular, and medial.',
  quiz: [
    { q: 'A patient has new unilateral calf swelling, warmth, and tenderness. The nurse should:', options: ['Massage the calf to improve circulation', 'Apply heat and ambulate the patient', 'Avoid manipulating the leg and notify the provider', 'Elevate and vigorously exercise the leg'], answer: 2, why: 'These are DVT signs. Manipulation risks dislodging a clot and causing pulmonary embolism.' },
    { q: 'Bilateral pitting edema of the lower legs most suggests:', options: ['Deep vein thrombosis', 'A systemic cause such as heart failure', 'Cellulitis', 'Local trauma'], answer: 1, why: 'Bilateral edema points to a systemic cause. Unilateral points to a local or vascular cause.' },
  ],
},
{
  id: 'feet', label: 'Ankles, Feet & Pedal Pulses', cat: 'vasc',
  pos: [[-0.105, 0.075, 0.075], [0.105, 0.075, 0.075]],
  technique: 'Inspect the feet and between the toes for color, lesions, ulcers, and nail condition — essential in diabetic patients. Palpate temperature. Locate the dorsalis pedis pulse on the dorsum of the foot and the posterior tibial behind the medial malleolus. Assess capillary refill, sensation (monofilament in diabetics), and range of motion.',
  normal: 'Feet warm, pink, and intact including between the toes. Dorsalis pedis and posterior tibial pulses 2+ and equal. Capillary refill under 3 seconds. Sensation intact. Full ROM.',
  watch: 'Cold, pale, pulseless, painful, paresthetic, paralyzed foot — the 6 Ps of acute arterial occlusion, a surgical emergency. Ulceration between or under the toes. Loss of protective sensation in diabetes. Thick yellow nails, fissures.',
  pearl: 'The 6 Ps of arterial occlusion: Pain, Pallor, Pulselessness, Paresthesia, Paralysis, Poikilothermia (cold). Always inspect BETWEEN the toes in diabetic patients — that is where ulcers hide.',
  quiz: [
    { q: 'Which finding in a post-operative extremity requires the MOST urgent escalation?', options: ['Mild swelling with intact pulses', 'Cool, pale foot with absent pulses and new numbness', 'Bruising around the incision', 'Discomfort with movement'], answer: 1, why: 'Cool, pale, pulseless, and numb suggests acute arterial occlusion or compartment syndrome — a limb-threatening emergency.' },
    { q: 'Where is the dorsalis pedis pulse palpated?', options: ['Behind the medial malleolus', 'On the dorsum of the foot lateral to the extensor hallucis longus tendon', 'In the popliteal fossa', 'Over the lateral malleolus'], answer: 1, why: 'Dorsalis pedis is on the top of the foot; posterior tibial is behind the medial malleolus.' },
  ],
},

/* ---------- 24. Neuro ---------- */
{
  id: 'neuro', label: 'Neurologic: Motor, Sensory, Reflexes', cat: 'neuro',
  pos: [[0.135, 0.46, 0.10]],
  technique: 'Assess mental status and orientation, then cranial nerves, then motor (strength, tone, pronator drift), then sensory (light touch, sharp/dull, vibration, proprioception, comparing side to side), then cerebellar function (finger-to-nose, heel-to-shin, rapid alternating movements, Romberg), then gait, then deep tendon reflexes (biceps, triceps, brachioradialis, patellar, Achilles) and plantar response.',
  normal: 'Alert and oriented x4. Strength 5/5 throughout, no pronator drift. Sensation intact and symmetric. Coordination intact, Romberg negative. Gait steady. DTRs 2+ and symmetric. Plantar response downgoing.',
  watch: 'Any new focal or asymmetric deficit. Pronator drift. Positive Babinski (upgoing great toe) in anyone over 2 years — an upper motor neuron sign. Ataxia, positive Romberg (fall risk). Declining GCS. Cushing triad (hypertension with widening pulse pressure, bradycardia, irregular respirations) is a LATE sign of raised intracranial pressure.',
  pearl: 'Glasgow Coma Scale: Eyes 4, Verbal 5, Motor 6, total 3-15. Under 8, intubate. Cushing triad is late and ominous — act on rising ICP long before it appears.',
  quiz: [
    { q: 'A positive Babinski sign in an adult indicates:', options: ['Normal reflex', 'Upper motor neuron lesion', 'Peripheral neuropathy', 'Cerebellar dysfunction'], answer: 1, why: 'Dorsiflexion of the great toe with fanning is normal under age 2 but indicates an upper motor neuron lesion in adults.' },
    { q: 'Hypertension with widening pulse pressure, bradycardia, and irregular respirations is:', options: ['Beck triad', 'Cushing triad — late sign of increased ICP', 'Septic shock', 'Normal post-operative variation'], answer: 1, why: 'Cushing triad is a late and ominous sign of raised intracranial pressure requiring emergent intervention.' },
    { q: 'What is the lowest possible Glasgow Coma Scale score?', options: ['0', '1', '3', '5'], answer: 2, why: 'GCS ranges 3-15; the minimum in each category is 1, so the floor is 3.' },
  ],
},

/* ---------- 25. GU ---------- */
{
  id: 'gu', label: 'Genitourinary', cat: 'gu',
  pos: [[0, 0.90, 0.125]],
  technique: 'Performed last, with a chaperone and full attention to privacy and consent. Inspect the suprapubic area and palpate or bladder-scan for distention. Assess urinary patterns, continence, and any catheter and its output. Inspect external genitalia for lesions, discharge, or irritation as clinically indicated. Assess perineal skin integrity.',
  normal: 'No suprapubic distention or tenderness. Voiding without difficulty; urine clear and yellow. External genitalia without lesions or discharge. Perineal skin intact.',
  watch: 'Bladder distention with inability to void (urinary retention — scan and consider catheterization). Cloudy, foul-smelling, or bloody urine. Output under 30 mL/hour (inadequate renal perfusion). Catheter-associated trauma or infection signs. Skin breakdown from incontinence.',
  pearl: 'Urine output under 30 mL/hour in an adult is a red flag for inadequate renal perfusion — report it. GU and rectal exams come last in the sequence for patient comfort and dignity.',
  quiz: [
    { q: 'Which urine output in an adult requires escalation?', options: ['60 mL/hour', '45 mL/hour', 'Less than 30 mL/hour', '100 mL/hour'], answer: 2, why: 'Below 30 mL/hour suggests inadequate renal perfusion or acute kidney injury and must be reported.' },
    { q: 'A post-operative patient has not voided in 8 hours and reports suprapubic pressure. The nurse should FIRST:', options: ['Insert a catheter immediately', 'Perform a bladder scan', 'Administer a diuretic', 'Encourage oral fluids and wait'], answer: 1, why: 'A non-invasive bladder scan confirms retention and volume before any invasive intervention.' },
  ],
},

];
