import streamlit as st
from connect_data_warehouse import query_job_listings
import matplotlib.pyplot as plt


def layout():
    st.set_page_config(layout="wide")
    st.title("HR Dashboard")
    st.write("Detta projekt implementerar en modern datastack för att lösa analysutmaningar för en rekryteringsbyrå. Vår lösning automatiserar utvinning, omvandling och analys av arbetsmarknadsdata från Arbetsförmedlingen för att hjälpa rekryteringsspecialister att fatta datadrivna beslut.")
    cols = st.columns(2)
    with cols[0]:
        tabel_options = {
            "Yrken med social inriktning": "marts.mart_social_job",
            "Yrken med teknisk inriktning": "marts.mart_technical_jobs",
            "Chefer och verksamhetsledare": "marts.mart_managers_job"
        }
        table = st.selectbox("Välj tabell", options=list(tabel_options.keys()))
        
        table = tabel_options[table]

        df = query_job_listings(tabel_name=table)

    with cols[1]:
        slider = st.slider("Välj antal filtrerade annonser", value=10, min_value=0, max_value=50, step=5)

    st.write("### KPI's")
    cols = st.columns(3)

    with cols[0]:
        st.metric("Antal annonser", value=df["VACANCIES"].sum(), border=True)

    with cols[1]:
        st.metric(label="Totalt i Stockholm", value = df.query("WORKPLACE_ADDRESS__MUNICIPALITY == 'Stockholm'")["VACANCIES"].sum(), border=True)

    with cols[2]:
        top_employer = df.groupby("EMPLOYER__NAME")["VACANCIES"].sum().sort_values(ascending=False).head(1)
        st.metric(label="Top 1 Arbetsgivare", value=top_employer.index[0], border=True)

    cols = st.columns(2)
    with cols[0]:
            st.markdown(f"### top {slider} arbetsgivare med flest annonser")

            top_employer_bar = (
                df.groupby("EMPLOYER__NAME")["VACANCIES"]
                .sum()
                .sort_values(ascending=False)
                .head(slider)
                .reset_index()
            )

            plt.figure(figsize=(9, 4))
            plt.barh(top_employer_bar["EMPLOYER__NAME"], top_employer_bar["VACANCIES"], color="#b660b0")
            plt.gca().invert_yaxis()
            plt.xlabel("Antal annonser", color="white", size=14)
            plt.ylabel("Arbetsgivare", color="white", size=14)
            plt.xticks(color="white")
            plt.yticks(color="white")

            st.pyplot(plt,transparent=True)
    
    with cols[1]:
        st.markdown(f"### Top {slider} yrkesgrupper med flest annonser")

        top_job_bar = (
                df.groupby("OCCUPATION_GROUP")["VACANCIES"]
                .sum()
                .sort_values(ascending=False)
                .head(slider)
                .reset_index()
            )

        plt.figure(figsize=(9, 4))
        plt.barh(top_job_bar["OCCUPATION_GROUP"], top_job_bar["VACANCIES"], color="#779bc4")
        plt.gca().invert_yaxis()
        plt.xlabel("Antal annonser", color="white", size=14)
        plt.ylabel("Yrkesgrupper", color="white", size=14)
        plt.xticks(color="white")
        plt.yticks(color="white")

        st.pyplot(plt,transparent=True)

    cols = st.columns(2)
    with cols[0]:
        st.markdown(f"### Top {slider} städer med flest annonser")
        county_bar = (
            df.groupby("WORKPLACE_ADDRESS__MUNICIPALITY")["VACANCIES"]
            .sum()
            .sort_values(ascending=False)
            .head(slider)
            .reset_index()
        )

        plt.figure(figsize=(9, 4))
        plt.barh(county_bar["WORKPLACE_ADDRESS__MUNICIPALITY"], county_bar["VACANCIES"], color="#78c477")
        plt.gca().invert_yaxis()
        plt.xlabel("Antal annonser", color="white", size=14)
        plt.ylabel("Län", color="white", size=14)
        plt.xticks(color="white")
        plt.yticks(color="white")

        st.pyplot(plt,transparent=True)

    with cols[1]:
        st.markdown(f"### Top {slider} yrkesgrupper med krav på körkort")
        
        df_license = df[df["DRIVING_LICENSE_REQUIRED"] == True]

        driving_bar = (
            df_license.groupby("OCCUPATION_GROUP")["VACANCIES"]
            .sum()
            .sort_values(ascending=False)
            .head(slider)
            .reset_index()
        )


        plt.figure(figsize=(9, 4))
        plt.barh(driving_bar["OCCUPATION_GROUP"], driving_bar["VACANCIES"], color="#c75656")
        plt.gca().invert_yaxis()
        plt.xlabel("Antal annonser med krav på körkort", color="white", size=14)
        plt.ylabel("Yrkesgrupp", color="white", size=14)
        plt.xticks(color="white")
        plt.yticks(color="white")

        st.pyplot(plt,transparent=True)


    st.write("### Hitta job")
    cols = st.columns(2)
    with cols[0]:
        municipality = st.selectbox("Välj stad", options=sorted(df["WORKPLACE_ADDRESS__MUNICIPALITY"].dropna().unique()))
    
    with cols[1]:
        employer_options = ["Alla"] + sorted(df.query("WORKPLACE_ADDRESS__MUNICIPALITY == @municipality")["EMPLOYER__NAME"].dropna().unique().tolist())
        employer_name = st.selectbox("Välj arbetsgivare", employer_options)


        df_filtered = df.query("WORKPLACE_ADDRESS__MUNICIPALITY == @municipality")
        if employer_name != "Alla":
            df_filtered = df_filtered.query("EMPLOYER__NAME == @employer_name")

    cols = st.columns(2)
    with cols[0]:
        st.metric(label="Totalta job", value = df_filtered["VACANCIES"].sum(), border=True)
    
    with cols[1]:
        top_jobs = (
        df_filtered.groupby("OCCUPATION_GROUP")["VACANCIES"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
        st.dataframe(top_jobs,hide_index=True)


    with st.expander("Se all data"):
        st.dataframe(df)

if __name__ == "__main__":
    layout()