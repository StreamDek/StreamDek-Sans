"""StreamDek Sans: original parametric outlines. No input font outlines.
Build: python build.py (fonttools, brotli, skia-pathops required).
Coordinates use a 1000-unit em, Cartesian y-up. See DESIGN.md.
"""
from pathlib import Path
import sys, math, unicodedata as ud, json, copy, time, io
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / 'font-build-deps'))
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.basePen import BasePen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.svgLib.path import parse_path
from fontTools.ttLib import TTFont, newTable
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor, InstanceDescriptor
from fontTools.varLib import build as build_variable
from fontTools.otlLib.builder import buildStatTable
from fontTools.ttLib.removeOverlaps import removeOverlaps

STYLES = {300:'Light',400:'Regular',500:'Medium',600:'SemiBold',700:'Bold',800:'ExtraBold'}
STROKES = {300:48,400:66,500:82,600:98,700:114,800:130}
# Every path below was drawn for this project. The stroke is converted to real
# filled contours; it is never a renderer's synthetic bold setting.
D = {}
def define(c,w,*paths): D[c]=(w,list(paths))
define('A',650,'M 72 36 L 320 664 L 578 36','M 165 245 L 477 245')
define('B',640,'M 100 36 L 100 664 L 310 664 C 560 664 562 382 322 382 L 100 382','M 312 382 C 602 382 604 36 316 36 L 100 36')
define('C',660,'M 567 578 C 518 646 450 675 340 675 C 179 675 87 545 87 350 C 87 155 179 25 340 25 C 450 25 519 61 577 132')
define('D',680,'M 100 36 L 100 664 L 306 664 C 505 664 596 541 596 350 C 596 159 505 36 306 36 Z')
define('E',570,'M 490 664 L 100 664 L 100 36 L 500 36','M 100 363 L 441 363')
define('F',550,'M 100 36 L 100 664 L 490 664','M 100 373 L 434 373')
define('G',700,'M 587 579 C 529 648 453 675 350 675 C 182 675 87 545 87 350 C 87 156 182 25 350 25 C 451 25 537 57 602 110 L 602 327 L 391 327')
define('H',700,'M 100 36 L 100 664','M 600 36 L 600 664','M 100 357 L 600 357')
define('I',340,'M 88 664 L 252 664','M 170 664 L 170 36','M 88 36 L 252 36')
define('J',520,'M 430 664 L 430 209 C 430 82 372 25 264 25 C 153 25 92 92 82 186')
define('K',620,'M 100 36 L 100 664','M 548 664 L 100 294','M 297 454 L 560 36')
define('L',530,'M 100 664 L 100 36 L 465 36')
define('M',830,'M 100 36 L 100 664 L 415 223 L 730 664 L 730 36')
define('N',710,'M 100 36 L 100 664 L 610 36 L 610 664')
define('O',710,'M 355 675 C 176 675 87 541 87 350 C 87 159 176 25 355 25 C 534 25 623 159 623 350 C 623 541 534 675 355 675 Z')
define('P',610,'M 100 36 L 100 664 L 308 664 C 574 664 574 334 308 334 L 100 334')
define('Q',710,*D['O'][1],'M 425 181 L 640 -48')
define('R',640,*D['P'][1],'M 323 334 L 573 36')
define('S',610,'M 512 578 C 466 646 399 675 305 675 C 165 675 91 598 91 505 C 91 285 523 400 523 193 C 523 94 445 25 302 25 C 199 25 121 63 76 132')
define('T',590,'M 61 664 L 529 664','M 295 664 L 295 36')
define('U',690,'M 100 664 L 100 258 C 100 97 181 25 345 25 C 509 25 590 97 590 258 L 590 664')
define('V',630,'M 66 664 L 315 36 L 564 664')
define('W',940,'M 70 664 L 254 36 L 470 596 L 686 36 L 870 664')
define('X',620,'M 80 664 L 540 36','M 540 664 L 80 36')
define('Y',620,'M 66 664 L 310 342 L 554 664','M 310 342 L 310 36')
define('Z',590,'M 83 664 L 507 664 L 83 36 L 517 36')
define('a',565,'M 114 432 C 171 487 220 498 282 498 C 400 498 464 435 464 332 L 464 36','M 459 281 C 402 303 343 317 277 317 C 144 317 88 258 88 174 C 88 82 161 25 264 25 C 366 25 430 89 464 143')
define('b',590,'M 99 724 L 99 36','M 99 259 C 99 406 173 495 290 495 C 421 495 506 405 506 260 C 506 115 421 25 290 25 C 173 25 99 114 99 259 Z')
define('c',540,'M 455 422 C 410 471 357 495 280 495 C 157 495 84 403 84 260 C 84 117 157 25 280 25 C 357 25 415 54 459 103')
define('d',590,'M 491 724 L 491 36','M 491 259 C 491 406 417 495 300 495 C 169 495 84 405 84 260 C 84 115 169 25 300 25 C 417 25 491 114 491 259 Z')
define('e',558,'M 93 279 L 470 279 C 478 408 408 495 284 495 C 154 495 84 398 84 260 C 84 111 173 25 295 25 C 373 25 424 50 466 94')
define('f',350,'M 147 36 L 147 572 C 147 678 197 729 282 729 L 326 729','M 57 478 L 302 478')
define('g',590,'M 491 484 L 491 -15 C 491 -150 416 -209 299 -209 C 221 -209 165 -189 122 -152','M 491 267 C 491 412 417 495 300 495 C 169 495 84 405 84 267 C 84 129 169 43 300 43 C 417 43 491 123 491 267 Z')
define('h',588,'M 99 36 L 99 724','M 99 292 C 99 425 181 495 290 495 C 418 495 489 421 489 289 L 489 36')
define('i',252,'M 126 36 L 126 484','M 126 652 L 126 656')
define('j',265,'M 156 484 L 156 -72 C 156 -169 109 -209 33 -209','M 156 652 L 156 656')
define('k',536,'M 99 36 L 99 724','M 451 484 L 101 184','M 267 327 L 469 36')
define('l',286,'M 106 724 L 106 129 C 106 57 143 36 214 36')
define('m',865,'M 99 36 L 99 484','M 99 309 C 99 431 164 495 263 495 C 362 495 429 430 429 310 L 429 36','M 429 309 C 429 431 494 495 593 495 C 699 495 766 430 766 310 L 766 36')
define('n',588,'M 99 36 L 99 484',D['h'][1][1])
define('o',586,'M 293 495 C 157 495 84 400 84 260 C 84 120 157 25 293 25 C 429 25 502 120 502 260 C 502 400 429 495 293 495 Z')
define('p',590,'M 99 -204 L 99 484',D['b'][1][1])
define('q',590,'M 491 -204 L 491 484',D['d'][1][1])
define('r',374,'M 99 36 L 99 484','M 99 280 C 99 424 185 495 278 495 C 300 495 318 492 332 486')
define('s',499,'M 408 424 C 366 472 314 495 250 495 C 145 495 88 438 88 371 C 88 212 415 298 415 149 C 415 70 349 25 245 25 C 168 25 109 52 74 100')
define('t',368,'M 145 650 L 145 153 C 145 63 185 25 260 25 C 287 25 308 29 327 38','M 52 478 L 315 478')
define('u',588,'M 99 484 L 99 231 C 99 99 170 25 298 25 C 407 25 489 95 489 228','M 489 484 L 489 36')
define('v',520,'M 69 484 L 260 36 L 451 484')
define('w',780,'M 65 484 L 213 36 L 390 447 L 567 36 L 715 484')
define('x',524,'M 77 484 L 447 36','M 447 484 L 77 36')
define('y',530,'M 68 484 L 274 40','M 463 484 L 236 -75 C 198 -173 156 -209 83 -209')
define('z',488,'M 78 484 L 410 484 L 78 36 L 418 36')
define('0',600,'M 300 675 C 162 675 105 558 105 350 C 105 142 162 25 300 25 C 438 25 495 142 495 350 C 495 558 438 675 300 675 Z','M 292 350 L 308 350')
define('1',600,'M 158 529 L 319 664 L 319 36','M 175 36 L 463 36')
define('2',600,'M 98 543 C 122 634 196 675 304 675 C 425 675 497 607 497 513 C 497 417 430 367 350 302 L 102 99 L 102 36 L 508 36')
define('3',600,'M 105 585 C 149 645 218 675 308 675 C 426 675 491 614 491 518 C 491 421 414 365 298 365','M 286 365 C 428 365 509 309 509 200 C 509 89 433 25 302 25 C 208 25 127 60 88 132')
define('4',600,'M 394 36 L 394 664 L 326 664 L 82 224 L 520 224')
define('5',600,'M 483 664 L 139 664 L 117 382 C 160 413 218 431 280 431 C 422 431 510 354 510 229 C 510 100 427 25 297 25 C 203 25 130 61 89 128')
define('6',600,'M 470 602 C 426 651 374 675 310 675 C 165 675 94 540 94 320 C 94 121 166 25 304 25 C 430 25 505 109 505 228 C 505 348 430 425 308 425 C 206 425 131 369 99 276')
define('7',600,'M 83 664 L 517 664 L 222 36')
define('8',600,'M 300 675 C 173 675 110 610 110 519 C 110 424 182 361 300 361 C 418 361 490 424 490 519 C 490 610 427 675 300 675 Z','M 300 361 C 164 361 90 296 90 198 C 90 91 164 25 300 25 C 436 25 510 91 510 198 C 510 296 436 361 300 361 Z')
define('9',600,'M 128 97 C 173 49 225 25 289 25 C 435 25 506 160 506 380 C 506 579 434 675 296 675 C 170 675 95 591 95 472 C 95 352 170 275 292 275 C 394 275 469 331 501 424')
define('.',250,'M 125 45 L 125 49')
define(',',250,'M 145 61 C 145 -5 128 -51 95 -84')
define(':',260,'M 130 405 L 130 409','M 130 45 L 130 49')
define(';',260,'M 130 405 L 130 409',D[','][1][0])
define('!',280,'M 140 664 L 140 223','M 140 45 L 140 49')
define('?',510,'M 85 553 C 107 633 170 675 263 675 C 367 675 435 613 435 523 C 435 413 255 385 255 269 L 255 221','M 255 45 L 255 49')
define('-',370,'M 81 274 L 289 274')
define('_',540,'M 65 -126 L 475 -126')
define('/',440,'M 72 -84 L 368 724')
define('\\',440,'M 72 724 L 368 -84')
define('|',250,'M 125 -174 L 125 754')
define('(',330,'M 255 747 C 135 637 83 489 83 300 C 83 111 135 -37 255 -147')
define(')',330,'M 75 747 C 195 637 247 489 247 300 C 247 111 195 -37 75 -147')
define('[',330,'M 250 724 L 110 724 L 110 -124 L 250 -124')
define(']',330,'M 80 724 L 220 724 L 220 -124 L 80 -124')
define('{',390,'M 311 724 C 178 724 173 672 173 556 L 173 422 C 173 338 135 300 77 300 C 135 300 173 262 173 178 L 173 44 C 173 -72 178 -124 311 -124')
define('}',390,'M 79 724 C 212 724 217 672 217 556 L 217 422 C 217 338 255 300 313 300 C 255 300 217 262 217 178 L 217 44 C 217 -72 212 -124 79 -124')
define("'",230,'M 115 664 L 115 512')
define('"',380,'M 112 664 L 112 512','M 268 664 L 268 512')
define('`',320,'M 100 720 L 228 610')
define('+',570,'M 88 300 L 482 300','M 285 497 L 285 103')
define('=',570,'M 88 403 L 482 403','M 88 197 L 482 197')
define('<',550,'M 451 515 L 98 300 L 451 85')
define('>',550,'M 99 515 L 452 300 L 99 85')
define('~',570,'M 82 286 C 188 426 346 174 488 314')
define('^',520,'M 86 409 L 260 664 L 434 409')
define('*',450,'M 225 686 L 225 351','M 65 570 L 384 466','M 126 383 L 324 654')
define('#',640,'M 250 694 L 159 6','M 473 694 L 382 6','M 94 469 L 568 469','M 72 231 L 546 231')
define('$',610,*D['S'][1],'M 305 754 L 305 -54')
define('%',850,'M 158 36 L 692 664','M 219 674 C 121 674 89 605 89 522 C 89 439 121 370 219 370 C 317 370 349 439 349 522 C 349 605 317 674 219 674 Z','M 631 330 C 533 330 501 261 501 178 C 501 95 533 26 631 26 C 729 26 761 95 761 178 C 761 261 729 330 631 330 Z')
define('&',705,'M 609 36 L 230 459 C 117 586 199 675 296 675 C 405 675 465 564 363 469 L 179 310 C 14 166 112 25 283 25 C 439 25 539 177 591 354')
define('@',910,'M 573 250 C 519 208 464 195 416 212 C 316 246 316 451 420 489 C 479 510 530 484 563 439','M 582 489 L 550 276 C 528 128 732 145 758 346 C 786 561 650 693 461 693 C 236 693 107 539 107 337 C 107 120 249 -23 463 -23 C 579 -23 672 11 733 67')
define(' ',285)
define('\u00a0',285)
define('€',650,*D['C'][1],'M 47 422 L 427 422','M 47 278 L 406 278')
define('£',600,'M 498 589 C 458 647 403 675 325 675 C 200 675 157 590 176 474 L 206 291 C 226 167 171 78 94 36 L 514 36','M 81 303 L 406 303')
define('¥',620,*D['Y'][1],'M 132 323 L 488 323','M 132 194 L 488 194')
define('¢',540,*D['c'][1],'M 310 612 L 236 -89')
define('¤',640,'M 320 526 C 197 526 124 450 124 350 C 124 250 197 174 320 174 C 443 174 516 250 516 350 C 516 450 443 526 320 526 Z','M 113 565 L 184 494','M 456 206 L 527 135','M 113 135 L 184 206','M 456 494 L 527 565')
define('ß',590,'M 99 36 L 99 522 C 99 669 170 729 288 729 C 399 729 472 661 472 566 C 472 490 423 435 353 407 C 459 369 510 307 510 206 C 510 87 435 25 326 25 L 256 25')
define('ı',252,'M 126 36 L 126 484')
define('ſ',350,*D['f'][1])
define('Ł',530,*D['L'][1],'M 44 254 L 299 464')
define('ł',286,*D['l'][1],'M 35 280 L 230 424')
define('Đ',680,*D['D'][1],'M 37 350 L 269 350')
define('đ',590,*D['d'][1],'M 332 627 L 571 627')
define('Ð',680,*D['Đ'][1])
define('ð',586,*D['o'][1],'M 152 703 C 387 649 501 475 502 260','M 195 565 L 391 715')
define('Þ',610,'M 100 36 L 100 724','M 100 540 L 308 540 C 574 540 574 210 308 210 L 100 210')
define('þ',590,'M 99 -204 L 99 724',D['b'][1][1])
define('Ø',710,*D['O'][1],'M 151 -12 L 559 712')
define('ø',586,*D['o'][1],'M 118 -13 L 468 533')
define('Æ',870,'M 61 36 L 377 664 L 770 664','M 463 664 L 463 36 L 789 36','M 166 249 L 463 249','M 463 365 L 738 365')
define('æ',869,*D['a'][1],'M 465 279 L 785 279 C 793 408 738 495 624 495 C 514 495 459 398 459 260 C 459 111 530 25 641 25 C 711 25 755 50 787 88')
define('Œ',960,'M 520 629 C 462 661 415 675 345 675 C 166 675 87 541 87 350 C 87 159 166 25 345 25 C 415 25 462 39 520 71','M 868 664 L 520 664 L 520 36 L 888 36','M 520 363 L 833 363')
define('œ',970,*D['o'][1],'M 505 279 L 885 279 C 893 408 823 495 699 495 C 569 495 499 398 499 260 C 499 111 588 25 710 25 C 788 25 839 50 881 94')
define('Ŋ',710,*D['N'][1],'M 610 36 L 610 -41 C 610 -162 543 -209 440 -209')
define('ŋ',588,*D['n'][1],'M 489 36 L 489 -41 C 489 -162 423 -209 320 -209')
define('Ħ',700,*D['H'][1],'M 32 553 L 668 553')
define('ħ',588,*D['h'][1],'M 30 618 L 263 618')
define('Ŧ',590,*D['T'][1],'M 141 399 L 449 399')
define('ŧ',368,*D['t'][1],'M 70 288 L 284 288')
define('ĸ',536,'M 99 36 L 99 484',*D['k'][1][1:])
define('ƒ',350,*D['f'][1],'M 147 36 L 147 -69 C 147 -170 109 -209 37 -209')
define('×',570,'M 109 479 L 461 121','M 461 479 L 109 121')
define('÷',570,*D['-'][1], 'M 285 477 L 285 481','M 285 119 L 285 123')
D['÷']=(570,['M 88 300 L 482 300',*D['÷'][1][1:]])
define('±',570,*D['+'][1],'M 88 -34 L 482 -34')
define('¬',570,'M 88 403 L 482 403 L 482 207')
define('°',360,'M 180 687 C 114 687 73 643 73 581 C 73 519 114 475 180 475 C 246 475 287 519 287 581 C 287 643 246 687 180 687 Z')
define('·',250,'M 125 284 L 125 288')
define('•',330,'M 143 284 L 187 284')
define('–',570,'M 72 274 L 498 274')
define('—',950,'M 72 274 L 878 274')
define('−',570,'M 88 300 L 482 300')
define('…',750,'M 125 45 L 125 49','M 375 45 L 375 49','M 625 45 L 625 49')
define('‘',250,'M 151 723 C 106 672 99 623 107 586')
define('’',250,'M 143 723 C 151 686 144 637 99 586')
define('‚',250,*D[','][1])
define('“',425,*D['‘'][1],'M 326 723 C 281 672 274 623 282 586')
define('”',425,*D['’'][1],'M 318 723 C 326 686 319 637 274 586')
define('„',425,*D[','][1],'M 320 61 C 320 -5 303 -51 270 -84')
define('‹',340,'M 247 449 L 95 274 L 247 99')
define('›',340,'M 93 449 L 245 274 L 93 99')
define('«',545,*D['‹'][1],'M 452 449 L 300 274 L 452 99')
define('»',545,*D['›'][1],'M 298 449 L 450 274 L 298 99')
define('†',440,'M 220 724 L 220 -54','M 70 487 L 370 487')
define('‡',440,*D['†'][1],'M 70 183 L 370 183')
define('§',560,'M 465 634 C 423 697 356 723 275 723 C 163 723 99 666 99 584 C 99 437 459 437 459 284 C 459 217 415 170 345 139','M 97 71 C 139 8 206 -18 287 -18 C 399 -18 463 39 463 121 C 463 268 103 268 103 421 C 103 488 147 535 217 566')
define('¶',610,'M 499 -154 L 499 664 L 260 664 C 44 664 44 351 260 351 L 328 351','M 328 664 L 328 -154')
define('µ',588,*D['u'][1],'M 99 231 L 99 -204')
define('∞',850,'M 425 300 C 197 654 77 451 77 300 C 77 149 197 -54 425 300 C 653 654 773 451 773 300 C 773 149 653 -54 425 300 Z')
define('←',800,'M 705 300 L 94 300 L 308 506','M 94 300 L 308 94')
define('→',800,'M 95 300 L 706 300 L 492 506','M 706 300 L 492 94')
define('↑',600,'M 300 33 L 300 666 L 94 452','M 300 666 L 506 452')
define('↓',600,'M 300 667 L 300 34 L 94 248','M 300 34 L 506 248')
define('≠',570,*D['='][1],'M 170 59 L 400 541')
define('≤',550,*D['<'][1],'M 99 -59 L 451 -59')
define('≥',550,*D['>'][1],'M 99 -59 L 451 -59')
define('√',650,'M 67 255 L 200 62 L 465 728 L 593 728')
define('¦',250,'M 125 754 L 125 383','M 125 217 L 125 -154')
define('¡',280,'M 140 474 L 140 478','M 140 300 L 140 -141')
define('¿',510,'M 255 474 L 255 478','M 255 302 L 255 254 C 255 138 75 110 75 0 C 75 -90 143 -152 247 -152 C 340 -152 403 -110 425 -30')

class SamplePen(BasePen):
    def __init__(self): super().__init__(None); self.paths=[]; self.p=[]
    def _moveTo(self,p): self.p=[p]
    def _lineTo(self,p): self.p.append(p)
    def _curveToOne(self,a,b,c):
        o=self.p[-1]
        for i in range(1,19):
            t=i/18; u=1-t
            self.p.append(tuple(u*u*u*o[j]+3*u*u*t*a[j]+3*u*t*t*b[j]+t*t*t*c[j] for j in [0,1]))
    def _qCurveToOne(self,a,b):
        o=self.p[-1]
        for i in range(1,13):
            t=i/12; u=1-t; self.p.append(tuple(u*u*o[j]+2*u*t*a[j]+t*t*b[j] for j in [0,1]))
    def _closePath(self):
        if self.p[-1]==self.p[0]: self.p.pop()
        self.paths.append((self.p,True)); self.p=[]
    def _endPath(self):
        if self.p: self.paths.append((self.p,False)); self.p=[]

def area(p): return sum(p[i-1][0]*p[i][1]-p[i][0]*p[i-1][1] for i in range(len(p)))/2
def smooth_polygon(p,r):
    # Round sharp corners only. Sampling/topology is weight-independent.
    out=[]
    for i,b in enumerate(p):
        a=p[i-1]; c=p[(i+1)%len(p)]
        la=math.dist(a,b); lc=math.dist(b,c)
        if la<.001 or lc<.001: out.append(b); continue
        ua=((a[0]-b[0])/la,(a[1]-b[1])/la); uc=((c[0]-b[0])/lc,(c[1]-b[1])/lc)
        d=min(r,la*.24,lc*.24)
        aa=(b[0]+ua[0]*d,b[1]+ua[1]*d); cc=(b[0]+uc[0]*d,b[1]+uc[1]*d)
        out.append(aa)
        for j in range(1,4):
            t=j/3; u=1-t; out.append((u*u*aa[0]+2*u*t*b[0]+t*t*cc[0],u*u*aa[1]+2*u*t*b[1]+t*t*cc[1]))
    return out

def stroke(points,closed,t):
    if not closed and len(points)==2 and math.dist(*points)<20:
        cx=(points[0][0]+points[1][0])/2; cy=(points[0][1]+points[1][1])/2
        return [[(cx+t*.58*math.cos(-i*math.tau/24),cy+t*.58*math.sin(-i*math.tau/24)) for i in range(24)]]
    ns=[]
    for a,b in zip(points,points[1:]+(points[:1] if closed else [])):
        dx=b[0]-a[0]; dy=b[1]-a[1]; l=math.hypot(dx,dy) or 1
        ns.append((-dy/l,dx/l))
    sides=[]
    for sign in (1,-1):
        side=[]
        for i,p in enumerate(points):
            if not closed and i==0: n=ns[0]
            elif not closed and i==len(points)-1: n=ns[-1]
            else:
                a=ns[i-1]; b=ns[i%len(ns)]; den=max(.22,1+a[0]*b[0]+a[1]*b[1]); n=((a[0]+b[0])/den,(a[1]+b[1])/den)
            side.append((p[0]+sign*t/2*n[0],p[1]+sign*t/2*n[1]))
        sides.append(side)
    if closed:
        polys=[sides[0],sides[1][::-1]]
        if abs(area(polys[0]))<abs(area(polys[1])): polys.reverse()
        if area(polys[0])>0: polys[0].reverse()
        if area(polys[1])<0: polys[1].reverse()
    else:
        # Flat terminal with a subtly rounded shoulder, no semicircular bubble.
        n0=ns[0]; ne=ns[-1]; start=(-n0[1],n0[0]); end=(ne[1],-ne[0]); e=t*.5
        sides[0][0]=(sides[0][0][0]+start[0]*e,sides[0][0][1]+start[1]*e)
        sides[1][0]=(sides[1][0][0]+start[0]*e,sides[1][0][1]+start[1]*e)
        sides[0][-1]=(sides[0][-1][0]+end[0]*e,sides[0][-1][1]+end[1]*e)
        sides[1][-1]=(sides[1][-1][0]+end[0]*e,sides[1][-1][1]+end[1]*e)
        polys=[sides[0]+sides[1][::-1]]
        if area(polys[0])>0: polys[0].reverse()
    return [smooth_polygon(p,t*.15) for p in polys]

def transform(polys,sx=1,sy=1,dx=0,dy=0): return [[(x*sx+dx,y*sy+dy) for x,y in p] for p in polys]
def draw_base(c,weight):
    w,paths=D[c]; polys=[]; t=STROKES[weight]
    # Preserve x-height and cap-height through all weights. Ascenders/descenders
    # follow the same transform; family line metrics remain fixed.
    height=520 if c.islower() and c not in 'ßſƒı' else 700
    sy=(height-t)/(height-72); dy=t/2-36*sy
    for path in paths:
        pen=SamplePen(); parse_path(path,pen)
        for pts,closed in pen.paths:
            pts=[(x,y*sy+dy) for x,y in pts]
            polys+=stroke(pts,closed,t)
    return w,polys

MARKS={
 '\u0300':['M -72 650 L 40 568'], '\u0301':['M -40 568 L 72 650'],
 '\u0302':['M -99 568 L 0 645 L 99 568'],
 '\u0303':['M -110 594 C -45 687 45 520 110 613'],
 '\u0304':['M -110 603 L 110 603'],
 '\u0306':['M -105 649 C -94 551 94 551 105 649'],
 '\u0307':['M 0 602 L 0 606'],
 '\u0308':['M -80 602 L -80 606','M 80 602 L 80 606'],
 '\u030a':['M 0 703 C -60 703 -76 666 -76 634 C -76 602 -60 565 0 565 C 60 565 76 602 76 634 C 76 666 60 703 0 703 Z'],
 '\u030b':['M -108 568 L -28 650','M 33 568 L 113 650'],
 '\u030c':['M -99 645 L 0 568 L 99 645'],
 '\u0327':['M 12 -19 L -25 -76 C 104 -52 112 -176 7 -185 C -27 -190 -54 -179 -69 -168'],
 '\u0328':['M 22 4 C -82 -80 -42 -166 53 -143'],
 '\u0326':['M 19 -90 C 19 -137 6 -171 -20 -195'],
 '\u0323':['M 0 -99 L 0 -95'],
 '\u0309':['M -37 634 C -8 700 86 658 41 613 L 1 582'],
}
def mark(c,weight):
    polys=[]
    for path in MARKS[c]:
        pen=SamplePen(); parse_path(path,pen)
        for pts,closed in pen.paths: polys+=stroke(pts,closed,STROKES[weight]*.78)
    return polys

def glyph(c,weight,stack=None):
    if c in D: return draw_base(c,weight)
    if c in MARKS: return 0,mark(c,weight)
    if c=='\u00ad': return D['-'][0],[]
    if c in '\u200b\u200c\u200d\u2060\ufeff': return 0,[]
    if c in '\u2002\u2003\u2009\u202f': return {'\u2002':500,'\u2003':1000,'\u2009':170,'\u202f':170}[c],[]
    if c in 'Ĳĳ':
        a,b=('I','J') if c=='Ĳ' else ('i','j'); wa,pa=glyph(a,weight); wb,pb=glyph(b,weight); return wa+wb,pa+transform(pb,dx=wa)
    if c in 'Ŀŀ':
        a='L' if c=='Ŀ' else 'l'; w,p=glyph(a,weight); _,q=glyph('·',weight); return w+140,p+transform(q,dx=w-50)
    if c=='ŉ':
        w,p=glyph('n',weight); _,q=glyph('’',weight); return w+125,transform(p,dx=125)+transform(q,sx=.7,sy=.7,dx=-25,dy=150)
    if c=='ẞ':
        w,p=glyph('ß',weight); return 650,transform(p,sx=1.09,sy=.96)
    if c in '¹²³⁰⁴⁵⁶⁷⁸⁹':
        num=str('⁰¹²³⁴⁵⁶⁷⁸⁹'.index(c)); w,p=glyph(num,weight); return 370,transform(p,sx=.58,sy=.58,dy=310)
    if c in '¼½¾':
        a,b={'¼':('1','4'),'½':('1','2'),'¾':('3','4')}[c]; _,p=glyph(a,weight); _,q=glyph(b,weight); _,r=glyph('/',weight)
        return 850,transform(p,sx=.55,sy=.55,dy=330)+transform(q,sx=.55,sy=.55,dx=490)+transform(r,sx=.65,sy=.75,dx=260,dy=70)
    if c in '©®℗':
        inner={'©':'C','®':'R','℗':'P'}[c]; _,q=glyph(inner,weight); _,p=glyph('O',weight)
        return 820,transform(p,sx=1.08,dx=27)+transform(q,sx=.48,sy=.48,dx=255,dy=183)
    if c in '™℠':
        a='T' if c=='™' else 'S'; wa,p=glyph(a,weight); wb,q=glyph('M',weight); return round((wa+wb)*.48),transform(p,sx=.48,sy=.48,dy=350)+transform(q,sx=.48,sy=.48,dx=wa*.48,dy=350)
    if c=='ª' or c=='º':
        w,p=glyph('a' if c=='ª' else 'o',weight); return round(w*.64),transform(p,sx=.64,sy=.64,dy=360)
    if c=='‰':
        w,p=glyph('%',weight); _,q=glyph('0',weight); return 1180,p+transform(q,sx=.44,sy=.44,dx=844,dy=10)
    if c=='ℓ': return glyph('l',weight)
    if c in '´¨¯¸˘˙˚˛ˇ˝':
        m={'´':'́','¨':'̈','¯':'̄','¸':'̧','˘':'̆','˙':'̇','˚':'̊','˛':'̨','ˇ':'̌','˝':'̋'}[c]
        return 370,transform(mark(m,weight),dx=185)
    dec=ud.normalize('NFD',c)
    if len(dec)>1 and dec[0] in D and all(m in MARKS for m in dec[1:]):
        base=dec[0]; w,p=glyph('ı' if base=='i' else base,weight)
        for j,m in enumerate(dec[1:]):
            below=ud.combining(m) in (202,220)
            y=0 if below else (205 if base.isupper() else 0)
            if j and not below: y+=140
            p+=transform(mark(m,weight),dx=w/2 + (w*.17 if m=='̨' else 0),dy=y)
        return w,p
    raise KeyError(c)

def gname(c): return 'uni%04X'%ord(c)
def inventory():
    candidates=set(D)|set(MARKS)|set('ĲĳĿŀŉẞ¹²³⁰⁴⁵⁶⁷⁸⁹¼½¾©®℗™℠ªº‰ℓ´¨¯¸˘˙˚˛ˇ˝\u00ad\u2002\u2003\u2009\u202f\u200b\u200c\u200d\u2060\ufeff')
    for cp in list(range(0xA0,0x180))+list(range(0x1E00,0x1F00))+[0x218,0x219,0x21a,0x21b]:
        c=chr(cp)
        try: glyph(c,400); candidates.add(c)
        except KeyError: pass
    return sorted(candidates,key=ord)

def draw(polys,pen):
    for p in polys:
        if len(p)<3: continue
        pen.moveTo(p[0])
        for q in p[1:]: pen.lineTo(q)
        pen.closePath()

def features(chars,widths):
    # Class kerning includes accented derivatives and preserves locale parity.
    groups={'A':'AÀÁÂÃÄÅĀĂĄǍ', 'V':'VWŴẀẂẄ', 'Y':'YÝŶŸỲ', 'T':'TŤŦȚ',
      'O':'OQCGÓÒÔÕÖØŌŎŐÇĆĈĊČĜĞĠĢ', 'a':'aàáâãäåāăą',
      'o':'oceqòóôõöøōŏőçćĉċčèéêëēĕėęě', 'v':'vwyýÿŷẁẃẅ',
      'L':'LĹĻĽŁ', 'P':'PF', 'r':'rŕŗř', 'dot':'.…,'}
    groups={k:[gname(c) for c in v if c in chars] for k,v in groups.items()}
    lines=['languagesystem DFLT dflt;','languagesystem latn dflt;']
    for k,v in groups.items(): lines.append('@K'+k+' = ['+' '.join(v)+'];')
    pairs=[('A','V',-45),('A','Y',-50),('A','T',-32),('V','A',-45),('V','a',-34),('V','o',-32),('Y','A',-50),('Y','a',-50),('Y','o',-52),('T','a',-38),('T','o',-42),('T','A',-32),('L','T',-27),('L','V',-30),('L','Y',-38),('P','A',-28),('P','dot',-52),('r','dot',-26),('v','dot',-33),('O','A',-10),('A','O',-10)]
    lines.append('feature kern {')
    for a,b,v in pairs: lines.append(f'pos @K{a} @K{b} {v};')
    lines.append('} kern;')
    lines.append('feature zero { sub uni0030 by zero.slash; } zero;')
    # Proportional numbers opt-in; default digits are tabular for timestamps.
    lines.append('feature pnum {')
    for c in '0123456789': lines.append(f'sub {gname(c)} by {gname(c)}.pnum;')
    lines.append('} pnum;')
    lines.append('feature tnum {')
    for c in '0123456789': lines.append(f'sub {gname(c)}.pnum by {gname(c)};')
    lines.append('} tnum;')
    for m in MARKS:
        cls='BOTTOM' if ud.combining(m) in (202,220) else 'TOP'
        anchor=0 if cls=='BOTTOM' else 520
        lines.append(f'markClass {gname(m)} <anchor 0 {anchor}> @MC_{cls};')
    lines.append('feature mark {')
    for c in chars:
        if c in MARKS or not c.isalpha(): continue
        top=725 if c.isupper() or c in 'bdfhkltß' else 520
        # Already accented base glyphs retain sensible stacked mark positions.
        decomp=ud.normalize('NFD',c)
        if len(decomp)>1 and any(ud.combining(x)==230 for x in decomp[1:]): top+=150
        lines.append(f'pos base {gname(c)} <anchor {widths[gname(c)]//2} {top}> mark @MC_TOP <anchor {widths[gname(c)]//2} 0> mark @MC_BOTTOM;')
    lines.append('} mark;')
    lines.append('feature mkmk {')
    for m in MARKS:
        cls='BOTTOM' if ud.combining(m) in (202,220) else 'TOP'
        y=-170 if cls=='BOTTOM' else 680
        lines.append(f'pos mark {gname(m)} <anchor 0 {y}> mark @MC_{cls};')
    lines.append('} mkmk;')
    return '\n'.join(lines)

def font(weight,chars,otf=False,clean=False):
    style=STYLES[weight]; outlines={}; widths={}
    notdef=[[(90,0),(90,700),(510,700),(510,0)],[(145,60),(455,60),(455,640),(145,640)]]
    outlines['.notdef']=notdef; widths['.notdef']=600
    for c in chars: widths[gname(c)],outlines[gname(c)]=glyph(c,weight)
    _,zero=draw_base('0',weight)
    # zero.slash removes the identifying centre dot before adding a slash.
    zero=zero[:-1]; zero+=stroke([(190,133),(410,567)],False,STROKES[weight]*.65)
    outlines['zero.slash']=zero; widths['zero.slash']=600
    for c in '0123456789':
        n=gname(c)+'.pnum'; shift=-72 if c=='1' else -8
        outlines[n]=transform(outlines[gname(c)],dx=shift); widths[n]=456 if c=='1' else 584
    order=list(outlines); fb=FontBuilder(1000,isTTF=not otf)
    fb.setupGlyphOrder(order); fb.setupCharacterMap({ord(c):gname(c) for c in chars})
    glyphs={}
    if not otf:
        for n,p in outlines.items():
            pen=TTGlyphPen(None); draw(p,pen); glyphs[n]=pen.glyph()
            if glyphs[n].numberOfContours>0: glyphs[n].flags[0]|=0x40
        fb.setupGlyf(glyphs)
    else:
        for n,p in outlines.items():
            pen=T2CharStringPen(widths[n],None); draw(p,pen); glyphs[n]=pen.getCharString()
        fb.setupCFF('StreamDekSans-'+style,{'FullName':'StreamDek Sans '+style,'FamilyName':'StreamDek Sans','Weight':style,'version':'0.900'},glyphs,{})
    metrics={n:(widths[n],round(min((x for p in pp for x,y in p),default=0))) for n,pp in outlines.items()}
    fb.setupHorizontalMetrics(metrics); fb.setupHorizontalHeader(ascent=1100,descent=-300,lineGap=0)
    # IDs 16/17 are the canonical family grouping. IDs 1/2 use legacy RIBBI
    # subfamilies so Windows installations expose all six real styles.
    legacy='StreamDek Sans' if weight in (400,700) else 'StreamDek Sans '+style
    fb.setupNameTable({'familyName':legacy,'styleName':'Bold' if weight==700 else 'Regular',
      'typographicFamily':'StreamDek Sans','typographicSubfamily':style,
      'uniqueFontIdentifier':f'StreamDekSans:0.900:{style}',
      'fullName':'StreamDek Sans '+style,'psName':'StreamDekSans-'+style,'version':'Version 0.900',
      'manufacturer':'StreamDek','designer':'Original StreamDek commission; generated with Codex',
      'description':'Original geometric sans with softly finished terminals. Review build 0.900.',
      'licenseDescription':'Custom StreamDek project assets. See LICENSE.txt supplied with this family.'})
    fb.setupOS2(version=4,sTypoAscender=1100,sTypoDescender=-300,sTypoLineGap=0,usWinAscent=1100,usWinDescent=300,
      usWeightClass=weight,usWidthClass=5,fsType=0,sxHeight=520,sCapHeight=700,
      fsSelection=(1<<7)|(1<<5 if weight==700 else (1<<6)),achVendID='STDK')
    fb.setupPost(); fb.font['head'].fontRevision=.900; fb.font['head'].macStyle=1 if weight==700 else 0
    fb.font['head'].created=fb.font['head'].modified=3874521600
    fb.font.recalcTimestamp=False
    fea=features(chars,widths); fb.addOpenTypeFeatures(fea)
    if not otf:
        gasp=newTable('gasp'); gasp.gaspRange={65535:15}; fb.font['gasp']=gasp
        if clean: removeOverlaps(fb.font,removeHinting=True)
    return fb.font,fea

def save_font(f,path):
    buf=io.BytesIO(); f.save(buf); payload=buf.getvalue()
    staged=path.with_name(path.name+'.tmp'); staged.write_bytes(payload)
    for attempt in range(20):
        try: staged.replace(path); return
        except PermissionError:
            if attempt==19: raise
            time.sleep(.5)

def main():
    chars=inventory()
    for folder in ['fonts/ttf','fonts/otf','fonts/woff2','fonts/variable','sources/masters','qa','specimens','docs','references']:
        (ROOT/folder).mkdir(parents=True,exist_ok=True)
    ds=DesignSpaceDocument(); axis=AxisDescriptor(); axis.name='Weight'; axis.tag='wght'; axis.minimum=300; axis.default=400; axis.maximum=800; ds.addAxis(axis)
    for weight,style in STYLES.items():
        print('Building',style,flush=True)
        f,fea=font(weight,chars); master=ROOT/'sources/masters'/f'StreamDekSans-{style}.ttf'
        s=SourceDescriptor(); s.path=str(master); s.name=style; s.familyName='StreamDek Sans'; s.styleName=style; s.location={'Weight':weight}; s.copyInfo=s.copyLib=s.copyFeatures=(weight==400); ds.addSource(s)
        inst=InstanceDescriptor(); inst.name=style; inst.familyName='StreamDek Sans'; inst.styleName=style; inst.location={'Weight':weight}; ds.addInstance(inst)
        if '--from-weight' in sys.argv and weight<int(sys.argv[sys.argv.index('--from-weight')+1]): continue
        save_font(f,master)
        static=copy.deepcopy(f); removeOverlaps(static,removeHinting=True); save_font(static,ROOT/'fonts/ttf'/f'StreamDekSans-{style}.ttf')
        static.flavor='woff2'; save_font(static,ROOT/'fonts/woff2'/f'StreamDekSans-{style}.woff2')
        # True CFF OTF from the cleaned TrueType outlines, not a renamed TTF.
        static.flavor=None; gs=static.getGlyphSet(); otf=FontBuilder(1000,isTTF=False)
        otf.setupGlyphOrder(static.getGlyphOrder()); otf.setupCharacterMap(static.getBestCmap()); cs={}
        from fontTools.pens.qu2cuPen import Qu2CuPen
        for name in static.getGlyphOrder():
            pen=T2CharStringPen(static['hmtx'][name][0],gs); gs[name].draw(Qu2CuPen(pen,max_err=1,all_cubic=True)); cs[name]=pen.getCharString()
        otf.setupCFF('StreamDekSans-'+style,{'FullName':'StreamDek Sans '+style,'FamilyName':'StreamDek Sans','Weight':style,'version':'0.900'},cs,{})
        for table in ['hmtx','hhea','name','OS/2','GPOS','GSUB','GDEF']:
            otf.font[table]=copy.deepcopy(static[table])
        otf.setupPost(); otf.font['head'].fontRevision=.900; otf.font['head'].macStyle=static['head'].macStyle
        otf.font['head'].created=otf.font['head'].modified=3874521600; otf.font.recalcTimestamp=False
        save_font(otf.font,ROOT/'fonts/otf'/f'StreamDekSans-{style}.otf')
    (ROOT/'sources/features.fea').write_text(fea,encoding='utf-8')
    ds.write(ROOT/'sources/StreamDekSans.designspace')
    print('Building variable',flush=True)
    vf,_,_=build_variable(str(ROOT/'sources/StreamDekSans.designspace'))
    buildStatTable(vf,[{'tag':'wght','name':'Weight','values':[{'value':w,'name':s,**({'flags':2,'linkedValue':700} if w==400 else {})} for w,s in STYLES.items()]}])
    vf['name'].setName('StreamDek Sans',1,3,1,0x409); vf['name'].setName('StreamDekSans-Variable',6,3,1,0x409)
    vf['name'].setName('StreamDek Sans',1,1,0,0); vf['name'].setName('StreamDekSans-Variable',6,1,0,0)
    vf.recalcTimestamp=False; save_font(vf,ROOT/'fonts/variable/StreamDekSans-Variable.ttf')
    vf.flavor='woff2'; save_font(vf,ROOT/'fonts/variable/StreamDekSans-Variable.woff2')
    (ROOT/'qa/coverage.json').write_text(json.dumps([{'codepoint':f'U+{ord(c):04X}','character':c,'name':ud.name(c,'UNNAMED')} for c in chars],ensure_ascii=False,indent=2),encoding='utf-8')
    print('DONE',len(chars),'mapped characters',flush=True)
if __name__=='__main__': main()
