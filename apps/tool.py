import streamlit as st
import pandas as pd
import numpy as np


def app():
    @st.cache
    # Load data
    def load_data():
        df = pd.read_csv("main_file_dataset.csv")
        # select only collection heads, with available year
        df_year = df[~df.Collection_Head.isnull()]
        df_year = df_year[~df_year.Year.isnull()]
        df_year = df_year[~df_year.Start.isnull()]
        #convert to numeric
        df_year.Start = pd.to_numeric(df_year.Start)
        df_year.End = pd.to_numeric(df_year.End)
        # select appropriate dates
        df_year = df_year[df_year.Start<df_year.End]
        df_year = df_year[(df_year.Start>1700) & (df_year.End>1700)]
        df_year["Country"] = df_year.Country.fillna("Unknown")
        df_year["Continent"] = df_year.Continent.fillna("Unknown")
        

        # create country to continent dictionary
        continent_list = df_year.Continent.unique()
        dic = {}
        for i in continent_list:
            dic[i] = set()
        for ind,row in df_year.iterrows():
            dic[row.Continent].add(row.Country)
        return df,df_year,dic
    files =  load_data()
    df =files[0]
    df_year = files[1]
    dic = files[2]

    def dataset_selector():
        dataset_container = st.sidebar.beta_expander(" Configure and Explore Dataset ", True)

        with dataset_container:
            st.header("Configure the Dataset for Exploration")
            if st.checkbox("See Caveats"):
                st.info("""Configuring the dataset selects rows with available date and text. While using this tool, only the rows which are collection headers (according to 
            our algorithm) and have existing date are used.
            """)
            values = st.slider("Choose time range", min_value=1700,max_value=1950,value=(1700,1950))
            start_date,end_date = values[0],values[1]
            author_identity = st.multiselect("Select Author Identity",options = (df_year.Author_Identity.unique()),
            default =df_year.Author_Identity.unique())
            author = st.selectbox("Select Author",options = np.append(np.array("All"),sorted(df_year.Name.unique())))
            continent = st.selectbox("Select Continent",options = np.append(np.array("All"),sorted(df_year.Continent.unique())))
            if continent!="All":
                country = st.selectbox("Select Country",np.append(np.array("All"),sorted(dic[continent])))
            else:
                country = "All"
            drawer_no = st.selectbox("Drawer No",options =np.append(np.array("All"), np.arange(157,232)))
            return start_date,end_date,author_identity,author,continent,country,drawer_no

    def generate_data(start_date, end_date,author_identity,author,continent,country,drawer_no):
        time_condition =(df_year.Start>=start_date) & (df_year.Start<=end_date)

        ret = df_year[time_condition]
        ret = ret[ret.Author_Identity.isin(author_identity)]

        if continent == "All":
            continent = df_year.Continent.unique()
        else:
            continent = [continent]
        ret = ret[ret.Continent.isin(continent)]

        if country == "All":
            country = df_year.Country.unique()
        else:
            country = [country]
        ret = ret[ret.Country.isin(country)]
  
        if drawer_no == "All":
            drawer_no = df_year.Drawer_No.unique()
        else:
            drawer_no = [int(drawer_no)]
        ret = ret[ret.Drawer_No.isin(drawer_no)]

        if author =="All":
            author = df_year.Name.unique()
        else:
            author = [author]
        ret = ret[ret.Name.isin(author)]

        columns = df_year.columns.tolist()
        if st.checkbox(" Select the columns to display:",False):
    
            columns_to_show = st.multiselect("",columns,default = columns)
            if len(columns_to_show) > 0:
                selected_df = ret[columns_to_show]
                return selected_df    
        return ret

    s = dataset_selector()
    first_exp= st.beta_expander("Explore Dataset",True)
    with first_exp:

        container1 = st.beta_container()
        with container1:
            first_container_displayed_df = generate_data(s[0],s[1],s[2],s[3],s[4],s[5],s[6])
            st.dataframe(first_container_displayed_df)


                   
     # Dictionaries with indices for history searching
    president_indices = {"York": [7072, 14590, 50164, 50170], "Craven": [2004, 2005, 9541, 10235, 11146, 11155, 11156, 11161, 11167, 11168, 11169, 11170, 11171, 11172, 11173, 11174, 11175, 11176, 11177, 11178, 11179, 11180, 11181, 11182, 11183, 11197, 11200, 14590, 15131, 19231, 20678, 20732, 21211, 25196, 27216, 48485], 
              "Gannaway": [6266, 6267, 6269, 16522, 41864], "Wood": [13320, 30929, 30984, 49501, 49528], 
              "Crowell": [127, 11387, 19234, 32886, 46573], "Kilgo": [158, 6815, 21326, 25715, 31143, 31930, 42066, 42069, 45697, 45808], 
              "Few": [4293, 4295, 5490, 5535, 6660, 7338, 7356, 13399, 13678, 13680, 14742, 15288, 15290, 15291, 15292, 15293, 15294, 15726, 17493, 17627, 17628, 17632, 18218, 21323, 26808, 28326, 32409, 34437, 34637, 35247, 42069, 46891, 47138, 47141], 
              "Flowers": [10743, 15710, 16296, 19004, 20519, 22959, 26399, 27309, 28173, 30657, 34052, 42059, 42065, 44500, 45697], 
            "Edens": [], "Hart": [14123], "Knight": [5490, 25741, 30171, 47829],
              "Sanford": [5490, 9533, 9541, 9554, 19873, 19875, 22266, 39311, 39312, 39313, 39314, 39363, 39364, 39365, 42007, 44948, 45317], 
              "Brodie": [], "Keohane": [], "Brodhead": [2619, 34442, 35593]}
    name_indices = {'brown': [], 'union': [31358, 50170], 'normal': [410, 2004, 4821, 5148, 5149, 6904, 7031, 9828, 15130, 15131, 15133, 20074, 20075, 25093, 25094, 25195, 44683, 47523, 47901, 48481, 48488], 'trinity': [127, 158, 932, 949, 1950, 2004, 2726, 4207, 4294, 4855, 4859, 5861, 5864, 5955, 6085, 6659, 6815, 6917, 6918, 6921, 7684, 7685, 7687, 7688, 7698, 7700, 8356, 9180, 9645, 10235, 10741, 10906, 10920, 11155, 11156, 11158, 11161, 11164, 11197, 11199, 11200, 11731, 11822, 12078, 13261, 13302, 13303, 13317, 13671, 13674, 14005, 15133, 16211, 17237, 17238, 17239, 17306, 17967, 19231, 19295, 19298, 19384, 20729, 20731, 21237, 21765, 22038, 22129, 22147, 22150, 22158, 23045, 24107, 24513, 24523, 24837, 25004, 25621, 25748, 27216, 27397, 27816, 27836, 28173, 28657, 28659, 28828, 30321, 30375, 30376, 30480, 30706, 30943, 30945, 30947, 30951, 31012, 31013, 31015, 31016, 31017, 31018, 31019, 31247, 31977, 32804, 32886, 34437, 34637, 34654, 35029, 35460, 37321, 37405, 37500, 37748, 37801, 38323, 38324, 39272, 39480, 39481, 39702, 40312, 40454, 40468, 40616, 40644, 40703, 41457, 41590, 41594, 41642, 41914, 42030, 42061, 42065, 42066, 42069, 42408, 42531, 42532, 42919, 42927, 43242, 43348, 43352, 43354, 43616, 43619, 44460, 44474, 44507, 44696, 45276, 45662, 45663, 45693, 45696, 45697, 45808, 46887, 47503, 47523, 49746, 49750, 49751, 50170, 50219], 'duke': [59, 60, 258, 415, 509, 515, 568, 570, 571, 572, 575, 577, 596, 749, 751, 752, 800, 878, 881, 888, 1084, 1085, 1408, 1432, 1594, 1619, 1941, 1950, 2095, 2168, 2178, 2388, 2820, 2829, 3592, 3885, 3912, 4139, 4143, 4273, 4294, 4463, 4465, 4466, 4467, 4471, 4472, 4504, 4664, 4665, 4860, 5148, 5149, 5231, 5488, 5489, 5610, 5730, 6085, 6086, 6090, 6106, 6116, 6122, 6185, 6186, 6236, 6265, 6434, 6551, 6565, 6630, 6773, 6777, 6844, 6986, 6990, 7021, 7337, 7484, 7683, 7688, 7701, 7974, 8023, 8085, 8090, 8093, 8185, 8191, 8251, 8356, 9038, 9179, 9180, 9260, 9273, 9404, 9405, 9407, 9410, 9412, 9414, 9417, 9419, 9420, 9645, 9663, 10329, 10354, 10386, 10504, 10662, 10743, 10752, 10753, 11037, 11045, 11168, 11175, 11197, 11337, 11735, 11737, 11823, 12145, 12152, 12533, 12561, 12679, 13053, 13141, 13302, 13318, 13655, 13669, 13692, 13693, 13694, 13695, 13696, 13741, 13743, 13745, 13746, 13747, 13750, 13751, 13752, 13753, 13754, 13755, 13756, 13757, 13758, 13759, 13760, 13761, 13762, 13763, 13764, 13765, 13766, 13767, 13768, 13769, 13770, 13771, 13772, 13773, 13774, 13775, 13776, 13777, 13778, 13779, 13780, 13781, 13782, 13783, 13793, 13795, 13796, 13797, 13798, 13799, 13800, 13801, 13806, 13807, 13808, 13809, 14399, 14484, 14512, 14516, 14517, 14585, 14623, 14861, 14979, 14983, 15294, 15511, 15697, 15751, 15752, 15927, 15939, 16184, 16278, 16529, 16542, 16556, 16557, 16797, 16842, 16922, 17179, 17472, 17493, 17494, 17497, 17498, 17754, 17756, 18432, 18666, 18712, 18713, 18952, 19185, 19309, 19311, 19334, 19384, 19444, 19616, 19647, 19648, 19650, 19651, 19652, 19653, 19658, 19660, 19662, 19666, 19771, 19865, 19909, 19912, 19920, 20156, 20210, 20212, 20214, 20318, 20523, 20542, 20549, 20823, 21005, 21396, 21508, 21566, 21616, 21723, 21815, 21954, 22050, 22265, 22266, 22267, 22272, 22285, 22594, 22595, 22597, 22618, 22772, 22868, 22869, 22871, 22893, 22895, 22905, 22921, 22922, 22923, 22926, 22943, 23288, 23343, 23775, 23909, 24166, 24237, 24525, 24619, 24838, 25049, 25074, 25251, 25262, 25263, 25264, 25665, 26306, 26307, 26393, 26398, 26399, 26603, 26801, 26854, 27338, 27340, 27457, 27486, 27719, 27720, 27790, 27802, 27889, 28247, 28561, 28601, 28658, 28718, 28828, 29203, 29456, 29573, 29623, 30375, 30376, 30650, 30666, 30677, 31230, 31322, 31509, 31813, 31892, 31899, 32183, 32297, 32343, 32851, 32877, 32971, 33042, 33092, 33642, 33672, 33917, 33922, 34078, 34080, 34136, 34437, 34537, 34539, 34654, 34850, 34882, 35029, 35030, 35031, 35234, 35237, 35251, 35367, 35373, 35418, 35620, 35990, 36033, 36215, 36299, 36493, 36495, 36496, 36542, 36652, 36711, 36804, 36868, 36869, 37052, 37205, 37214, 37221, 37260, 37261, 37263, 37405, 37612, 37613, 37656, 37657, 37801, 37847, 37849, 38056, 38063, 38064, 38071, 38235, 38401, 38412, 38679, 38866, 39017, 39135, 39255, 39258, 39271, 39294, 39295, 39297, 39311, 39313, 39314, 39673, 39675, 39679, 39680, 39681, 39744, 39745, 39747, 39748, 40073, 40076, 40077, 40078, 40080, 40082, 40083, 40235, 40319, 40337, 40338, 40616, 40703, 40878, 40952, 40978, 41173, 41174, 41568, 41644, 41703, 41736, 41775, 42007, 42051, 42069, 42377, 42533, 42780, 42991, 42994, 43032, 43238, 43242, 43243, 43244, 43247, 43338, 43348, 43352, 43369, 43370, 43417, 43598, 43599, 43616, 43760, 43762, 43763, 43996, 44012, 44200, 44245, 44447, 44459, 44513, 44535, 44812, 44857, 44859, 45317, 45318, 45704, 45710, 45866, 46093, 46469, 46470, 46473, 46685, 47102, 47152, 47173, 47272, 47601, 47703, 47864, 47880, 47979, 48169, 48439, 48644, 48709, 49487, 49585, 49586, 49592, 49716, 50170]}
    charleston = [ 1295, 11346, 12237, 12465, 12498, 12499, 12820, 16096, 21313,
            24542, 35513, 36175, 37469]
    wil = [9038, 9039, 9040, 9041, 9044, 11353, 11354]
    
    def get_df_key_index(key,dic):
        if key=="All":
            return df.iloc[sum(dic.values(), [])]
        ind = dic[key]
        return df.iloc[ind,:]

    def dataset_selector():
        dataset_container = st.sidebar.beta_expander("""Explore Collections Related to Duke's History & Other Interests""",False)
        choice = ["Duke University Presidents",
            "Duke University Early Names","Charleston Earthquake", "Wilmington Race Riot of 1898"]
        with dataset_container:
            check = st.radio("Explore",choice)
            if check ==choice[0]:
                duke_pres = st.selectbox("Select Duke University President ",np.append(np.array("All"),sorted(list(president_indices.keys()))))
                return duke_pres,0
            elif check == choice[1]:
                duke_uni = st.selectbox("Select Duke University's Early Names ",
                 np.append(np.array("All"),sorted(list(name_indices.keys()))))
                return duke_uni,1
            elif check == choice[2]:
                return None,"Charleston"
            else:
                return None, "Wilmington"
                
         

    def generate_data(selected_identity,explore_topic):
        if(explore_topic==0):
            exp_df = get_df_key_index(selected_identity,president_indices)
        elif(explore_topic==1):
            exp_df = get_df_key_index(selected_identity,name_indices)
        elif explore_topic=="Charleston":
            return df.iloc[charleston,:]
        else:
            return df.iloc[wil,:]
        return exp_df

    selected_identity,explore_topic = dataset_selector()

    second_exp = st.beta_expander("Explore Selected Colletions",False)
    with second_exp:
        container2 = st.beta_container()
        with container2:
            second_container_displayed_df =generate_data(selected_identity,explore_topic)
            st.dataframe(second_container_displayed_df)










    


# app()