// import utils from './utils';
// const utils = require('utils');
// const parse = require('node-html-parser');
/* -------------------------------------------------------------------------- */
/*                                   Tinymce                                  */
/* -------------------------------------------------------------------------- */

// const tinymceInit = () => {
  if (window.tinymce) {
    const tinymces = document.querySelectorAll('.tinymce');
    if (tinymces.length) {
      window.tinymce.execCommand('mceFocus', false, 'course-description');
      window.tinymce.init({
        selector: '.tinymce',
        height: '50vh',
        menubar: false,
        skin: utils.settings.tinymce.theme,
        content_style: `.mce-content-body { color: ${utils.getGrays().black} }`,
        mobile: {
          theme: 'mobile',
          toolbar: ['undo', 'bold'],
        },
        statusbar: false,
        plugins: 'link,image,lists,table,media, codesample',
        codesample_languages: [
          {text:'HTML/XML',value:'markup'},
          {text:"XML",value:"xml"},
          {text:"HTML",value:"html"},
          {text:"mathml",value:"mathml"},
          {text:"SVG",value:"svg"},
          {text:"CSS",value:"css"},
          {text:"Clike",value:"clike"},
          {text:"Javascript",value:"javascript"},
          {text:"ActionScript",value:"actionscript"},
          {text:"apacheconf",value:"apacheconf"},
          {text:"apl",value:"apl"},
          {text:"applescript",value:"applescript"},
          {text:"asciidoc",value:"asciidoc"},
          {text:"aspnet",value:"aspnet"},
          {text:"autoit",value:"autoit"},
          {text:"autohotkey",value:"autohotkey"},
          {text:"bash",value:"bash"},
          {text:"basic",value:"basic"},
          {text:"batch",value:"batch"},
          {text:"c",value:"c"},
          {text:"brainfuck",value:"brainfuck"},
          {text:"bro",value:"bro"},
          {text:"bison",value:"bison"},
          {text:"C#",value:"csharp"},
          {text:"C++",value:"cpp"},
          {text:"CoffeeScript",value:"coffeescript"},
          {text:"ruby",value:"ruby"},
          {text:"d",value:"d"},
          {text:"dart",value:"dart"},
          {text:"diff",value:"diff"},
          {text:"docker",value:"docker"},
          {text:"eiffel",value:"eiffel"},
          {text:"elixir",value:"elixir"},
          {text:"erlang",value:"erlang"},
          {text:"fsharp",value:"fsharp"},
          {text:"fortran",value:"fortran"},
          {text:"git",value:"git"},
          {text:"glsl",value:"glsl"},
          {text:"go",value:"go"},
          {text:"groovy",value:"groovy"},
          {text:"haml",value:"haml"},
          {text:"handlebars",value:"handlebars"},
          {text:"haskell",value:"haskell"},
          {text:"haxe",value:"haxe"},
          {text:"http",value:"http"},
          {text:"icon",value:"icon"},
          {text:"inform7",value:"inform7"},
          {text:"ini",value:"ini"},
          {text:"j",value:"j"},
          {text:"jade",value:"jade"},
          {text:"java",value:"java"},
          {text:"JSON",value:"json"},
          {text:"jsonp",value:"jsonp"},
          {text:"julia",value:"julia"},
          {text:"keyman",value:"keyman"},
          {text:"kotlin",value:"kotlin"},
          {text:"latex",value:"latex"},
          {text:"less",value:"less"},
          {text:"lolcode",value:"lolcode"},
          {text:"lua",value:"lua"},
          {text:"makefile",value:"makefile"},
          {text:"markdown",value:"markdown"},
          {text:"matlab",value:"matlab"},
          {text:"mel",value:"mel"},
          {text:"mizar",value:"mizar"},
          {text:"monkey",value:"monkey"},
          {text:"nasm",value:"nasm"},
          {text:"nginx",value:"nginx"},
          {text:"nim",value:"nim"},
          {text:"nix",value:"nix"},
          {text:"nsis",value:"nsis"},
          {text:"objectivec",value:"objectivec"},
          {text:"ocaml",value:"ocaml"},
          {text:"oz",value:"oz"},
          {text:"parigp",value:"parigp"},
          {text:"parser",value:"parser"},
          {text:"pascal",value:"pascal"},
          {text:"perl",value:"perl"},
          {text:"PHP",value:"php"},
          {text:"processing",value:"processing"},
          {text:"prolog",value:"prolog"},
          {text:"protobuf",value:"protobuf"},
          {text:"puppet",value:"puppet"},
          {text:"pure",value:"pure"},
          {text:"python",value:"python"},
          {text:"q",value:"q"},
          {text:"qore",value:"qore"},
          {text:"r",value:"r"},
          {text:"jsx",value:"jsx"},
          {text:"rest",value:"rest"},
          {text:"rip",value:"rip"},
          {text:"roboconf",value:"roboconf"},
          {text:"crystal",value:"crystal"},
          {text:"rust",value:"rust"},
          {text:"sas",value:"sas"},
          {text:"sass",value:"sass"},
          {text:"scss",value:"scss"},
          {text:"scala",value:"scala"},
          {text:"scheme",value:"scheme"},
          {text:"smalltalk",value:"smalltalk"},
          {text:"smarty",value:"smarty"},
          {text:"SQL",value:"sql"},
          {text:"stylus",value:"stylus"},
          {text:"swift",value:"swift"},
          {text:"tcl",value:"tcl"},
          {text:"textile",value:"textile"},
          {text:"twig",value:"twig"},
          {text:"TypeScript",value:"typescript"},
          {text:"verilog",value:"verilog"},
          {text:"vhdl",value:"vhdl"},
          {text:"wiki",value:"wiki"},
          {text:"YAML",value:"yaml"}
      ],
        toolbar:
          'bold italic link bullist numlist image table undo redo codesample',
        directionality: utils.getItemFromStore('isRTL') ? 'rtl' : 'ltr',
        theme_advanced_toolbar_align: 'center',
        setup: (editor) => {
          editor.on('change', () => {
            window.tinymce.triggerSave();
          });
        },
      });
    }

    const themeController = document.body;
    themeController &&
      themeController.addEventListener(
        'clickControl',
        ({ detail: { control } }) => {
          if (control === 'theme') {
            window.tinyMCE.editors.forEach((el) => {
              el.dom.addStyle(
                `.mce-content-body{color: ${
                  utils.getGrays().black
                } !important;}`
              );
            });
          }
        }
      );
  }
// };

// export default tinymceInit;
