# Imports
from typing import Dict, List

class UrlValidate:

    def __init__(
        self,
        tabs: Dict[str, str]
    ) -> None:
        '''
            UrlValidate is used as parent to validate an URL tabs and subtabs.

            Parameters:
                tabs: Dict[str, str]. Key is the page name and value the translation to the URL.
        '''
        self.__TABS = tabs

    @property
    def tabs(self):
        return self.__TABS

    def get_subtabs(
        self,
        tab: str
    ) -> Dict[str, str]:
        '''
            Returns all subtabs from a tab.
        '''
        ...

    def get_available_tabs_and_subtabs(
        self
    ) -> Dict[str, List[str]]:
        '''
            Returns all tabs and subtabs.
        '''
        to_ret: Dict[str, List[str]] = {}
        tabs: List[str] = self.get_tabs().keys()
        for tab in tabs:
            to_ret[tab] = list(self.get_subtabs(tab).keys())
        return to_ret
    
    def validate_tab(
        self,
        tab: str
    ) -> bool:
        '''
            Validate if the input tab is in current tabs.
        '''
        tab: str = tab.lower()
        if tab not in list(self.tabs.keys()):
            return False
        return True

    def validate_subtab(
        self,
        tab: str,
        subtab: str
    ) -> bool:
        '''
            Validate if the input subtab is in input tab subtabs.
        '''
        tab: str = tab.lower()
        subtab: str = subtab.lower() if subtab is not None else subtab
        if not self.validate_tab(tab):
            return False
        subtabs = self.get_subtabs(tab)
        if len(subtabs.keys())>0:
            if subtab not in subtabs:
                return False
        else:
            return subtab is None
        return True
    
    def validate_tab_and_subtabs(
        self,
        tab: str,
        subtab: str
    ) -> bool:
        '''
            Validate both tab and subtab.
        '''
        tab: str = tab.lower()
        subtab: str = subtab.lower() if subtab is not None else subtab
        if not self.validate_tab(tab):
            return False
        if not self.validate_subtab(tab, subtab):
            return False
        return True
    