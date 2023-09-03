# Data Anonymisation Project - Clinical Data Management 

### Project description and rationale:
- Anonymisation is the practice of removing identifying information from data in order to protect individuals' privacy and is critical to ensure sensitive information is kept secure.
- In this project, we aim to create an anonymised dataset by removing personally identifiable information from the original dataset whilst attempting to retain its utility and insights for 3 main stakeholders as per the project brief (refer to **CDM_Coursework_2.pdf**).
- We utilized k-anonymity, a privacy model that quantifies the anonymity of subjects in the dataset
    - Attributes are suppressed/generalized until each row is identical with at least k-1 rows
    - At worst, an individual can be narrowed down to a group of k individuals
 
### Methods used:
- Classifing the data into direct identifiers, quasi-identifiers and sensitive data to choose appropriate anonymisation methods
- Using a one-way cryptographic hash algorithm "SHA-2” using a unique direct identifier to create a reference table containing hashed attribute, key and salt
- Data banding into time-intervals, broader categories and partial postcodes
- Data perturbation - addition of Gaussian noise with a randomized number
- Data encryption using AES (Advanced Encryption Standard)

The Jupyter Notebook with the following code can be found in the **Dataset.Anonymisation.ipynb** file. 

