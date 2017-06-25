$(document).ready(function(){

    // Apply "selected" class to the currently selected option for a form-group
    // (removing from any previously selected option)
    function highlightSelected() {
        if (this.checked) {
            $(this).closest(".form-group").find('input[type="radio"]').parent().removeClass("selected");
            $(this).parent().addClass("selected");
        }
    }

    // Radio buttons need to become highlighted when selected as well as start
    // highlighted if already selected
    $('input[type="radio"]').change(highlightSelected).each(highlightSelected);


    // Submit annotation button is disabled initially */
    $('#annotation-form button').prop('disabled', true);

    
    // Enable submit form button when form has been filled out
    $('input[type="radio"]').change(function() {
        if ($('input[type="radio"]:checked').length == 3) {
            $('#annotation-form button').prop('disabled', false);
        }
    });

    // Q2
    $('.radio [for="id_loc_type_0"]').attr({'title':'eg for a query "Hotel in Perth", the location is explicit, given by a place name (Perth) that could be detected by a computer if supplied with a Gazetteer (a list of place names). Similarly, the location is explicit in the query "Real Madrid", even though this is not a query that should be answered by a map in most cases.'});
    $('.radio [for="id_loc_type_1"]').attr({'title':'eg for a query "Hairdresser near work" the query has an explicit location reference ("work"), although this one is subjective/individual, and is not expressed as a place name. These place references are, however, easily interpretable by people.'});
    $('.radio [for="id_loc_type_2"]').attr({'title':'for queries "Cafe" or "Office job", the location is not explicit, but would be understood by a person hearing this question and interpreted as "Cafe near me", or "Office job in this city". Similarly, a reference to a "romantic place" would fit here.'});
    $('.radio [for="id_loc_type_3"]').attr({'title':'for queries that are not spatial or do not include a reference to any place.'});

    // Q3
    $('.radio [for="id_query_type0"]').attr({'title':'"My goal is to go to specific known website that I already have in mind. The only reason I\'m searching is that it\'s more convenient than typing the URL, or perhaps I don\'t know the URL." Examples: "gumtree", "qantas"'});
    $('.radio [for="id_query_type1"]').attr({'title':'"I want to get an answer to a question that has a single, unambiguous answer. "Example: "Africa larger than Asia", "When is the supermarket open?", "30m to inches", "How to get to the airport?"'});
    $('.radio [for="id_query_type2"]').attr({'title':'"I want to get an answer to an open-ended question, or one with unconstrained depth." Examples: "Why are metals shiny", "Medicine XY side effects".'});    
    $('.radio [for="id_query_type3"]').attr({'title':'"I want to learn anything/everything about my topic. A query for topic X might be interpreted as "tell me about X." "Examples: "color blindness", "jfk jr".'});    
    $('.radio [for="id_query_type4"]').attr({'title':'"I want to get advice, ideas, suggestions, or instructions. " Examples: "help quitting smoking", "how to fix bike tyre".'});    
    $('.radio [for="id_query_type5"]').attr({'title':'"My goal is to find out whether/where some real world service or product can be obtained" Examples: "Hilton Sydney", "locksmith CBD", "XY brand" (in a store).'});    
    $('.radio [for="id_query_type6"]').attr({'title':'"My goal is to get a list of plausible suggested web sites (I.e. the search result list itself), each of which might be candidates for helping me achieve some underlying, unspecified goal" Examples: "best comedies 2016", "US National parks", "Westfield stores".'});    
    $('.radio [for="id_query_type7"]').attr({'title':'"My goal is to download a resource that must be on my computer or other device to be useful" Examples: "Word", "firefox".'});    
    $('.radio [for="id_query_type8"]').attr({'title':'"My goal is to be entertained simply by viewing items available on the result page " Examples: "weather cam mt buller", "tour the france live".'});    
    $('.radio [for="id_query_type9"]').attr({'title':'"My goal is to interact with a resource using another program/service available on the web site I find " Examples: "weather sydney", "flights".'});    
    $('.radio [for="id_query_type10"]').attr({'title':'"My goal is to obtain a resource that does not require a computer to use. I may print it out, but I can also just look at it on the screen. I\'m not obtaining it to learn some information, but because I want to use the resource itself". Example: "harry potter 2 pdf".'});
    $('.radio [for="id_query_type11"]').attr({'title':'"My goal is to be able to explore a map of an area. I do do not want a specific location, or list of locations, but rather, want to view a particular region.".'});
});
