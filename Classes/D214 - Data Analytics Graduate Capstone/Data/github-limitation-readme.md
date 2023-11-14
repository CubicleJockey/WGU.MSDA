# [GitHub](https://github.com/) file-size [limitation](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)


>File size limits
>GitHub limits the size of files allowed in repositories. If you attempt to add or update a file that is larger than 50 MiB, you will receive a warning from Git. The changes will still successfully push to your repository, but you can consider removing the commit to minimize performance impact. For more information, see "Removing files from a repository's history."
>
>>Note: If you add a file to a repository via a browser, the file can be no larger than 25 MiB. For more information, see "Adding a file to a repository."
>
>GitHub blocks files larger than 100 MiB.



## FILE SPLIT NOTES

`0-enron-emails-labeled.csv` and `1-enron-emails-labeled.csv` are a result of splitting the orginal dataset to get around
the [`GitHub`](https://github.com) file size limit.

Because of this limitation the original dataset what was download from Kaggle was split in half and will be put back
together via code.
