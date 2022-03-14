import re
from typing import List, Union


token_filter = {
    re.compile("\\xa0"): {
        "action": "remove"
    },
    re.compile("\\xa0.+"): {
        "action": "strip", 
        "strip_pattern":  re.compile("\\xa0")
    },
    re.compile("\-\-") :  {
        "action": "replace", 
        "replacement": [
            {
                "value": "<interrupt>",
                "case": lambda x, y: x == y,
                "description": "if the token is the last token"
            },
            {
                "value": "<pause>",
                "case": lambda x, y: x < y,
                "description": "the token is not the last token"

            }
        ]
    }
}

def split_by_delims(orig:str, 
                    delims: Union[list, str] = [".", "?", "!", ";"], 
                    filter: dict = None, return_string: bool=False) -> Union[list, str]:
    """
    Breaks an input string into a set of strings by using a list of
    delimiters or a pattern string. This also filters the set of
    output strings using a filter dictionary. 
    See the example filter for usage hints

    Parameters
    -----------
    orig: str
        the original string
    delims: Union[list, str]
        a list of delimiters or a string pattern. If a list is
        provided, each delimiter will be escaped before compiling
        to a pattern
    filter: dict
        a dictionary of filters. Each key should be a string or
        a re._pattern_type. 

        Example:
        {
            match_pattern : {
                action: one of [remove, strip, replace],
                // if strip and match pattern == re._pattern_type
                // provide a strip_pattern
                strip_pattern: {pattern},
                // if replace, provide a list of replacements
                replacement: [
                    {
                        // must contain a value
                        value: replacement_value, 
                        // optional - can contain a case, which is a lambda
                        case: lambda ..., 
                        // optional - description
                        description: "description..."
                    } 
                ]

            }
        }
    
    return_string: bool
        if True, returns the output sequence as a string instead of a list of splits
        defaults to False

    Returns
    --------
    a list or str
       
    """
    if type(delims) == list:
        expr = "[{}]".format("".join([re.escape(x) for x in delims]))
        pat = re.compile(expr)
    else:
        # pattern provided as a string
        pat = re.compile(delims)
    splits = re.split(pat, orig)
    length = len(splits)

    if filter:
        outs = []
        for i, s in enumerate(splits):
            out = s
            for k, v in filter.items():
                if isinstance(k, re._pattern_type):
                    match = re.match(k, s)
                    if match:
                        if v["action"] == "strip":
                            new_token = re.sub(v["strip_pattern"], "", s)
                            out = new_token
                        elif v["action"] == "replace":
                            if len(v["replacement"]) > 1:
                                for r in v["replacement"]:
                                    case = r["case"]
                                    if case(i, length -1 ):
                                        out = r["value"]
                                        break
                            else:
                                out = v["replacement"][0]["value"]
                        elif v["action"] == "remove":
                            out = None
                else:
                    if s == k:
                        if v["action"] == "strip":
                            out = s.strip(k)
                        elif v["action"] == "replace":
                            out = v["replacement"]
                        elif v["action"] == "remove":
                            out = None
            if out:
                outs.append(out)
        if return_string:
            return " ".join(outs)
        else:
            return outs
    
    if return_string:
        return " ".join(splits)
    else:
        return splits


def remove_time_stamps(input_text):
    text = ""
    lines = input_text.split("\n")
    for line in lines:
        if re.search('^WALLACE|BIDEN|TRUMP', line) is None and re.search('^[0-9]+:[0-9]{2}', line) is None and re.search('^$', line) is None:
            text += ' ' + line
        text = text.lstrip()
    return text