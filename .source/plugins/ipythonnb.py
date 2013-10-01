import os
from pelican import signals

try:
    from pelican.readers import BaseReader  # new Pelican API
except ImportError:
    from pelican.readers import Reader as BaseReader

try:
    from pelican.readers import EXTENSIONS  # old Pelican API
except ImportError:
    EXTENSIONS = None

try:
    import json
    import markdown

    from IPython.config import Config
    from IPython.nbconvert.exporters import HTMLExporter

    from IPython.nbconvert.filters.highlight import _pygment_highlight
    from pygments.formatters import HtmlFormatter
except Exception as e:
    IPython = False
    raise e


CUSTOM_CSS = """
<style type="text/css">
.cell.border-box-sizing.code_cell.vbox {
  border-left 1px solid red;
}
img {
    border: 0;
}
pre.ipynb {
    padding: 3px 9.5px;
}
pre {
    font-size: 0.80em;
    overflow: visible;
    padding: 0px;
    margin-left: 0px;
    border: none;
}
div.cell{border:0px solid transparent;display:-webkit-box;-webkit-box-orient:vertical;-webkit-box-align:stretch;display:-moz-box;-moz-box-orient:vertical;-moz-box-align:stretch;display:box;box-orient:vertical;box-align:stretch;width:100%;padding:5px 5px 5px 0px;margin:2px 0px 2px 7px;outline:none;}div.cell.selected{border-radius:4px;border:0 #ababab solid;}
.border-box-sizing{box-sizing:border-box;-moz-box-sizing:border-box;-webkit-box-sizing:border-box;}
.code_cell .ctb_prompt{display:block;}
.vbox{display:-webkit-box;-webkit-box-orient:vertical;-webkit-box-align:stretch;display:-moz-box;-moz-box-orient:vertical;-moz-box-align:stretch;display:box;box-orient:vertical;box-align:stretch;width:100%;}
.vbox>*{-webkit-box-flex:0;-moz-box-flex:0;box-flex:0;}
div.input_area{border:0px solid #cfcfcf;border-radius:4px;background:none;margin-top:8px;}
.ctb_show .input_area,.ctb_show .ctb_hideshow+div.text_cell_input{border-top-right-radius:0px;border-top-left-radius:0px;}
.hbox{display:-webkit-box;-webkit-box-orient:horizontal;-webkit-box-align:stretch;display:-moz-box;-moz-box-orient:horizontal;-moz-box-align:stretch;display:box;box-orient:horizontal;box-align:stretch;}
.hbox>*{-webkit-box-flex:0;-moz-box-flex:0;box-flex:0;}
div.prompt{width:11ex;padding:0.4em;margin:0px;font-family:monospace;text-align:right;line-height:1.231em;} /*!!!!!!!!FIXME*/
div.input_prompt{color:navy;border-top:0px solid transparent;}
span.input_prompt{font-family:inherit;}
.box-flex1{-webkit-box-flex:1;-moz-box-flex:1;box-flex:1;}

div.output_wrapper{
    margin-top:5px;
    position:relative;
    display:-webkit-box;
    -webkit-box-orient:vertical;
    -webkit-box-align:stretch;
    display:-moz-box;
    -moz-box-orient:vertical;
    -moz-box-align:stretch;
    display:box;
    box-orient:vertical;
    box-align:stretch;
    width:100%;
}
div.output_area{padding:0px;page-break-inside:avoid;display:-webkit-box;-webkit-box-orient:horizontal;-webkit-box-align:stretch;display:-moz-box;-moz-box-orient:horizontal;-moz-box-align:stretch;display:box;box-orient:horizontal;box-align:stretch;}
div.output_area pre{
    font-family:monospace;
    margin:0;
    padding:0;
    border:0;
    font-size:100%;
    vertical-align:baseline;
    color:black;
    background-color:transparent;
    -webkit-border-radius:0;
    -moz-border-radius:0;
    border-radius:0;
    line-height:inherit;
}
div.output_prompt{color:darkred;}
div.output_subarea{
    font-size: 0.80em;
    padding:0.44em 0.4em 0.4em 1px;
    margin-left:6px;
    -webkit-box-flex:1;
    -moz-box-flex:1;
    box-flex:1;
}

.highlight-ipynb .hll { background-color: #ffffcc }
.highlight-ipynb  { background: none; }
.highlight-ipynb .c { color: #408080; font-style: italic } /* Comment */
.highlight-ipynb .err { border: 1px solid #FF0000 } /* Error */
.highlight-ipynb .k { color: #008000; font-weight: bold } /* Keyword */
.highlight-ipynb .o { color: #666666 } /* Operator */
.highlight-ipynb .cm { color: #408080; font-style: italic } /* Comment.Multiline */
.highlight-ipynb .cp { color: #BC7A00 } /* Comment.Preproc */
.highlight-ipynb .c1 { color: #408080; font-style: italic } /* Comment.Single */
.highlight-ipynb .cs { color: #408080; font-style: italic } /* Comment.Special */
.highlight-ipynb .gd { color: #A00000 } /* Generic.Deleted */
.highlight-ipynb .ge { font-style: italic } /* Generic.Emph */
.highlight-ipynb .gr { color: #FF0000 } /* Generic.Error */
.highlight-ipynb .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.highlight-ipynb .gi { color: #00A000 } /* Generic.Inserted */
.highlight-ipynb .go { color: #888888 } /* Generic.Output */
.highlight-ipynb .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.highlight-ipynb .gs { font-weight: bold } /* Generic.Strong */
.highlight-ipynb .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.highlight-ipynb .gt { color: #0044DD } /* Generic.Traceback */
.highlight-ipynb .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.highlight-ipynb .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.highlight-ipynb .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.highlight-ipynb .kp { color: #008000 } /* Keyword.Pseudo */
.highlight-ipynb .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.highlight-ipynb .kt { color: #B00040 } /* Keyword.Type */
.highlight-ipynb .m { color: #666666 } /* Literal.Number */
.highlight-ipynb .s { color: #BA2121 } /* Literal.String */
.highlight-ipynb .na { color: #7D9029 } /* Name.Attribute */
.highlight-ipynb .nb { color: #008000 } /* Name.Builtin */
.highlight-ipynb .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.highlight-ipynb .no { color: #880000 } /* Name.Constant */
.highlight-ipynb .nd { color: #AA22FF } /* Name.Decorator */
.highlight-ipynb .ni { color: #999999; font-weight: bold } /* Name.Entity */
.highlight-ipynb .ne { color: #D2413A; font-weight: bold } /* Name.Exception */
.highlight-ipynb .nf { color: #0000FF } /* Name.Function */
.highlight-ipynb .nl { color: #A0A000 } /* Name.Label */
.highlight-ipynb .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.highlight-ipynb .nt { color: #008000; font-weight: bold } /* Name.Tag */
.highlight-ipynb .nv { color: #19177C } /* Name.Variable */
.highlight-ipynb .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.highlight-ipynb .w { color: #bbbbbb } /* Text.Whitespace */
.highlight-ipynb .mf { color: #666666 } /* Literal.Number.Float */
.highlight-ipynb .mh { color: #666666 } /* Literal.Number.Hex */
.highlight-ipynb .mi { color: #666666 } /* Literal.Number.Integer */
.highlight-ipynb .mo { color: #666666 } /* Literal.Number.Oct */
.highlight-ipynb .sb { color: #BA2121 } /* Literal.String.Backtick */
.highlight-ipynb .sc { color: #BA2121 } /* Literal.String.Char */
.highlight-ipynb .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.highlight-ipynb .s2 { color: #BA2121 } /* Literal.String.Double */
.highlight-ipynb .se { color: #BB6622; font-weight: bold } /* Literal.String.Escape */
.highlight-ipynb .sh { color: #BA2121 } /* Literal.String.Heredoc */
.highlight-ipynb .si { color: #BB6688; font-weight: bold } /* Literal.String.Interpol */
.highlight-ipynb .sx { color: #008000 } /* Literal.String.Other */
.highlight-ipynb .sr { color: #BB6688 } /* Literal.String.Regex */
.highlight-ipynb .s1 { color: #BA2121 } /* Literal.String.Single */
.highlight-ipynb .ss { color: #19177C } /* Literal.String.Symbol */
.highlight-ipynb .bp { color: #008000 } /* Name.Builtin.Pseudo */
.highlight-ipynb .vc { color: #19177C } /* Name.Variable.Class */
.highlight-ipynb .vg { color: #19177C } /* Name.Variable.Global */
.highlight-ipynb .vi { color: #19177C } /* Name.Variable.Instance */
.highlight-ipynb .il { color: #666667 } /* Literal.Number.Integer.Long */

.cell.border-box-sizing.code_cell.vbox {
  margin-left: 40px;
  border-left: 3px solid #abc;
}

</style>
"""


def custom_highlighter(source, language='ipython'):
    formatter = HtmlFormatter(cssclass='highlight-ipynb')
    output = _pygment_highlight(source, formatter, language)
    return output.replace('<pre>', '<pre class="ipynb">')


class iPythonNB(BaseReader):
    enabled = True
    file_extensions = ['ipynb']

    def read(self, filepath):
        filedir = os.path.dirname(filepath)
        filename = os.path.basename(filepath)

        _metadata = {}
        # See if metadata file exists metadata
        metadata_filename = filename.split('.')[0] + '.ipynb-meta'
        metadata_filepath = os.path.join(filedir, metadata_filename)
        if os.path.exists(metadata_filepath):
            with open(metadata_filepath, 'r') as metadata_file:
                content = metadata_file.read()
                metadata_file = open(metadata_filepath)
                md = markdown.Markdown(extensions=['meta'])
                md.convert(content)
                _metadata = md.Meta

            for key, value in _metadata.items():
                _metadata[key] = value[0]
        else:
            # Try to load metadata from inside ipython nb
            ipynb_file = open(filepath)
            _metadata = json.load(ipynb_file)['metadata']

        metadata = {}
        for key, value in _metadata.items():
            key = key.lower()
            metadata[key] = self.process_metadata(key, value)
        metadata['ipython'] = True

        # Converting ipythonnb to html
        config = Config({'CSSHTMLHeaderTransformer': {'enabled': True, 'highlight_class': '.highlight-ipynb'}})
        exporter = HTMLExporter(config=config, template_file='basic', filters={'highlight2html': custom_highlighter})
        body, info = exporter.from_filename(filepath)

        def filter_tags(s):
            l = s.split('\n')
            exclude = ['a', '.rendered_html', '@media']
            l = [i for i in l if len(list(filter(i.startswith, exclude))) == 0]
            ans = '\n'.join(l)
            return STYLE_TAG.format(ans)

        STYLE_TAG = '<style type=\"text/css\">{0}</style>'
        body = CUSTOM_CSS + body
        return body, metadata


def add_reader(arg):
    if EXTENSIONS is None:  # new pelican API:
        arg.settings['READERS']['ipynb'] = iPythonNB
    else:
        EXTENSIONS['ipynb'] = iPythonNB


def register():
    signals.initialized.connect(add_reader)
