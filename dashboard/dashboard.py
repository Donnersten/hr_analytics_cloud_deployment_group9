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
        st.metric("Antal annonser", value=df["vacancies"].sum(), border=True)

    with cols[1]:
        st.metric(label="Totalt i Stockholm", value=df.query("workplace_address__municipality == 'Stockholm'")["vacancies"].sum(), border=True)

    with cols[2]:
        top_employer = df.groupby("EMPLOYER__NAME")["vacancies"].sum().sort_values(ascending=False).head(1)
        st.metric(label="Top 1 Arbetsgivare", value=top_employer.index[0], border=True)

    cols = st.columns(2)
    with cols[0]:
        st.markdown(f"### Top {slider} arbetsgivare med flest annonser")
        top_employer_bar = (
            df.groupby("EMPLOYER__NAME")["vacancies"]
            .sum()
            .sort_values(ascending=False)
            .head(slider)
            .reset_index()
        )

        plt.figure(figsize=(9, 4))
        plt.barh(top_employer_bar["EMPLOYER__NAME"], top_employer_bar["vacancies"], color="#b660b0")
        plt.gca().invert_yaxis()
        plt.xlabel("Antal annonser", color="white", size=14)
        plt.ylabel("Arbetsgivare", color="white", size=14)
        plt.xticks(color="white")
        plt.yticks(color="white")
        st.pyplot(plt, transparent=True)
    
    with cols[1]:
        st.markdown(f"### Top {slider} yrkesgrupper med flest annonser")
        top_job_bar = (
            df.groupby("occupation_group")["vacancies"]
            .sum()
            .sort_values(ascending=False)
            .head(slider)
            .reset_index()
        )

        plt.figure(figsize=(9, 4))
        plt.barh(top_job_bar["occupation_group"], top_job_bar["vacancies"], color="#779bc4")
        plt.gca().invert_yaxis()
        plt.xlabel("Antal annonser", color="white", size=14)
        plt.ylabel("Yrkesgrupper", color="white", size=14)
        plt.xticks(color="white")
        plt.yticks(color="white")
        st.pyplot(plt, transparent=True)

    cols = st.columns(2)
    with cols[0]:
        st.markdown(f"### Top {slider} städer med flest annonser")
        county_bar = (
            df.groupby("workplace_address__municipality")["vacancies"]
            .sum()
            .sort_values(ascending=False)
            .head(slider)
            .reset_index()
        )

        plt.figure(figsize=(9, 4))
        plt.barh(county_bar["workplace_address__municipality"], county_bar["vacancies"], color="#78c477")
        plt.gca().invert_yaxis()
        plt.xlabel("Antal annonser", color="white", size=14)
        plt.ylabel("Kommun", color="white", size=14)
        plt.xticks(color="white")
        plt.yticks(color="white")
        st.pyplot(plt, transparent=True)

    with cols[1]:
        st.markdown(f"### Top {slider} yrkesgrupper med krav på körkort")
        df_license = df[df["driving_license_required"] == True]
        driving_bar = (
            df_license.groupby("occupation_group")["vacancies"]
            .sum()
            .sort_values(ascending=False)
            .head(slider)
            .reset_index()
        )

        plt.figure(figsize=(9, 4))
        plt.barh(driving_bar["occupation_group"], driving_bar["vacancies"], color="#c75656")
        plt.gca().invert_yaxis()
        plt.xlabel("Antal annonser med krav på körkort", color="white", size=14)
        plt.ylabel("Yrkesgrupp", color="white", size=14)
        plt.xticks(color="white")
        plt.yticks(color="white")
        st.pyplot(plt, transparent=True)

    st.write("### Hitta jobb")
    cols = st.columns(2)
    with cols[0]:
        municipality = st.selectbox("Välj stad", options=sorted(df["workplace_address__municipality"].dropna().unique()))
    
    with cols[1]:
        employer_options = ["Alla"] + sorted(df.query("workplace_address__municipality == @municipality")["EMPLOYER__NAME"].dropna().unique().tolist())
        employer_name = st.selectbox("Välj arbetsgivare", employer_options)

        df_filtered = df.query("workplace_address__municipality == @municipality")
        if employer_name != "Alla":
            df_filtered = df_filtered.query("EMPLOYER__NAME == @employer_name")

    cols = st.columns(2)
    with cols[0]:
        st.metric(label="Totala jobb", value=df_filtered["vacancies"].sum(), border=True)
    
    with cols[1]:
        top_jobs = (
            df_filtered.groupby("occupation_group")["vacancies"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )
        st.dataframe(top_jobs, hide_index=True)

    with st.expander("Se all data"):
        st.dataframe(df)


if __name__ == "__main__":
    layout()
