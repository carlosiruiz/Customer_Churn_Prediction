{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    " def to_binary(column):\n",
    "    \"\"\"\n",
    "    Takes in a column and turns its value from a Yes or No to a binary. \n",
    "    \n",
    "    \"\"\"\n",
    "    conditions=[\n",
    "        (customer_df[column].str.lower()=='yes'),            \n",
    "        (customer_df[column].str.lower()=='no'),\n",
    "    ]\n",
    "    choises=[\n",
    "        1,\n",
    "        0,\n",
    "\n",
    "    ]\n",
    "    customer_df[column]=np.select(conditions,choises,default=0)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def remove_dups(lists):\n",
    "    \"\"\"\n",
    "    Takes in a list of duplicated columns with the same name and removes the duplicated column and creates a\n",
    "    new column with a new name and values assigned.\n",
    "    \n",
    "    Once that is complete it drops column from dataframe.\n",
    "    \n",
    "    \"\"\"\n",
    "    for i in range(len(lists)):\n",
    "        \n",
    "        customer_df[\"tel_\"+lists[i]]=customer_df[lists[i]].iloc[:,1:2]\n",
    "        \n",
    "        customer_df.drop(lists[i],axis=1,inplace=True)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
